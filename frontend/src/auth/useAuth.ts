// src/auth/useAuth.ts
import {
  EventType,
  PublicClientApplication,
  type AccountInfo,
  type Configuration,
  type SilentRequest,
} from '@azure/msal-browser'
import { computed, ref } from 'vue'

// Dohvaćanje varijabli iz .env datoteke: import.meta.env.VITE_* (važno je da varijabla počinje prefiksom VITE_)
// Client ID (app registration) i Tenant ID (Azure AD tenant) imaju iste vrijednosti za sva okruženja.
// No, kako se radi o donekle povjerljivim podacima, ne želimo ih imati kao dio git koda.
// Ne bi bio ozbiljan problem da se nalaze u kodu jer će biti vidljivi u JavaScriptu koji se šalje klijentu.

const clientId = import.meta.env.VITE_CLIENT_ID
const tenantId = import.meta.env.VITE_TENANT_ID

const msalConfig: Configuration = {
  auth: {
    clientId,
    authority: `https://login.microsoftonline.com/${tenantId}`,
    redirectUri: window.location.origin,
  },
  cache: { cacheLocation: 'sessionStorage' },
}

const tokenRequest: SilentRequest = {
  // Kod izrade App Registration odabrali smo ime access_as_user za 'scope' koje je bilo arbitratno, sad je važno da koristimo isto ime
  scopes: [`api://${clientId}/access_as_user`],
}

let msalInstance: PublicClientApplication | null = null
const accounts = ref<AccountInfo[]>([])
const isAuthenticated = computed(() => accounts.value.length > 0)
const account = computed(() => accounts.value[0] ?? null)

export async function initAuth() {
  // Ova funkcija poziva se samo jednom (u main.ts) i inicijalizira globalne varijable u ovoj datoteci.
  msalInstance = new PublicClientApplication(msalConfig)
  await msalInstance.initialize()

  // Kad Azure završi login proces, preusmjerava preglednik na našu aplikaciju.
  // U tom slučaju MSAL treba pročitati postavljene parametre u URL-u i obraditi ih.
  // Ovo želimo napraviti prije inicijalizacije Vue aplikacije, jer bi Azureovi URL parametri (`http://localhost:5173?code=...#state=...`)  mogli zbuniti našu aplikaciju.
  try {
    await msalInstance.handleRedirectPromise()
  } catch (error) {
    // Npr. Azure odbije zahtjev (krivi scope/resource). Ne želimo da cijela aplikacija
    // ostane na bijelom ekranu — logiramo grešku i svejedno nastavljamo s mountanjem.
    console.error('handleRedirectPromise failed:', error)
  }
  accounts.value = msalInstance.getAllAccounts()

  msalInstance.addEventCallback((event) => {
    if (event.eventType === EventType.LOGIN_SUCCESS ||
        event.eventType === EventType.ACQUIRE_TOKEN_SUCCESS) {
      accounts.value = msalInstance!.getAllAccounts()
    }
    if (event.eventType === EventType.LOGOUT_SUCCESS) {
      accounts.value = []
    }
  })
}

function login() {
  // tokenRequest sadrži api://.../access_as_user; MSAL sam dodaje openid/profile/email.
  // Tako consent za API scope dobijemo već pri prijavi, pa kasniji acquireTokenSilent uspijeva.
  msalInstance!.loginRedirect(tokenRequest)
}

function logout() {
  msalInstance!.logoutRedirect()
}

async function getApiToken(): Promise<string> {
  // ID token sadrži podatke o korisniku, ali ne i dopuštenja koja korisnik ima za pojedini API.
  // Zbog toga kad šaljemo zahtjeve vanjskim servisima (uključujući i naš API), trebamo access token.
  try {
    const response = await msalInstance!.acquireTokenSilent({
      ...tokenRequest,
      account: account.value!,
    })
    return response.accessToken
  } catch (error) {
    // Silent može pasti zbog isteklog/nepostojećeg refresh tokena ili nedostatka consenta
    // za API scope (MSAL to ne klasificira uvijek kao InteractionRequiredAuthError), pa na
    // bilo koji neuspjeh padamo na interaktivni redirect. Ovim pozivom browser napušta
    // trenutnu stranicu, pa kod nakon njega praktički ne dolazi do izvršavanja.
    await msalInstance!.acquireTokenRedirect({ ...tokenRequest, account: account.value ?? undefined })
    throw error
  }
}

export function useAuth() {
  return { isAuthenticated, account, login, logout, getApiToken }
}
