// src/auth/useAuth.ts
import {
  EventType,
  InteractionRequiredAuthError,
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
  await msalInstance.handleRedirectPromise()
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
  msalInstance!.loginRedirect({ scopes: ['openid', 'profile', 'email'] })
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
    if (error instanceof InteractionRequiredAuthError) {
      // Preusmjerava na login; ovim pozivom završava cijela naša skripta jer browser napušta trenutnu stranicu
      await msalInstance!.acquireTokenRedirect(tokenRequest)
    }
    throw error
  }
}

export function useAuth() {
  return { isAuthenticated, account, login, logout, getApiToken }
}
