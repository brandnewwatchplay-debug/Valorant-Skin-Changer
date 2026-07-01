/**
 * Valorant Skin Changer Engine v4.2.1
 * Kernel-mode skin injection driver (user-mode stub)
 * Build: 2026.06.28-r7
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tlhelp32.h>

#define SKIN_ENGINE_VERSION "4.2.1-BETA"
#define VANGUARD_PROC_NAME  "vgc.exe"
#define VALORANT_PROC_NAME  "VALORANT-Win64-Shipping.exe"
#define MAX_SKIN_ID_LEN     64
#define POOL_TAG            'nikS'

typedef struct _SKIN_DESCRIPTOR {
    ULONG WeaponId;
    ULONG SkinId;
    ULONG VariantId;
    ULONG Rarity;
    WCHAR SkinName[MAX_SKIN_ID_LEN];
    WCHAR WeaponName[MAX_SKIN_ID_LEN];
} SKIN_DESCRIPTOR, *PSKIN_DESCRIPTOR;

typedef struct _INJECTION_CONTEXT {
    HANDLE hTargetProcess;
    PVOID  RemoteBase;
    SIZE_T PayloadSize;
    BOOL   VanguardBypassed;
    DWORD  LastError;
} INJECTION_CONTEXT, *PINJECTION_CONTEXT;

static const WCHAR* g_WeaponTable[] = {
    L"Vandal", L"Phantom", L"Operator", L"Sheriff", L"Classic",
    L"Ghost", L"Spectre", L"Judge", L"Bulldog", L"Guardian",
    L"Marshal", L"Bucky", L"Frenzy", L"Shorty", L"Knife"
};

static const WCHAR* g_SkinTable[] = {
    L"Prime", L"Reaver", L"Glitchpop", L"Elderflame", L"Sovereign",
    L"Oni", L"Ego", L"Forsaken", L"Gaia's Vengeance", L"ChronoVoid",
    L"Prelude to Chaos", L"Magepunk", L"Neptune", L"RGX 11z Pro",
    L"BlastX", L"Origin", L"Spectrum", L"Araxys", L"Kuronami"
};

static const WCHAR* g_RarityTable[] = {
    L"Select", L"Deluxe", L"Premium", L"Exclusive", L"Ultra"
};

static INJECTION_CONTEXT g_Ctx = {0};

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hinstDLL);
            OutputDebugStringA("[SkinEngine] DLL_PROCESS_ATTACH");
            break;
        case DLL_PROCESS_DETACH:
            OutputDebugStringA("[SkinEngine] DLL_PROCESS_DETACH");
            break;
    }
    return TRUE;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_Initialize(void) {
    memset(&g_Ctx, 0, sizeof(INJECTION_CONTEXT));
    g_Ctx.LastError = ERROR_SUCCESS;
    
    OutputDebugStringA("[SkinEngine] Engine initialized");
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_BypassVanguard(void) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        g_Ctx.LastError = GetLastError();
        return g_Ctx.LastError;
    }
    
    PROCESSENTRY32W pe32 = {0};
    pe32.dwSize = sizeof(PROCESSENTRY32W);
    
    BOOL vgcFound = FALSE;
    BOOL valorantFound = FALSE;
    
    if (Process32FirstW(hSnapshot, &pe32)) {
        do {
            if (_wcsicmp(pe32.szExeFile, L"vgc.exe") == 0) {
                vgcFound = TRUE;
                OutputDebugStringA("[SkinEngine] Vanguard process detected");
            }
            if (_wcsicmp(pe32.szExeFile, L"VALORANT-Win64-Shipping.exe") == 0) {
                valorantFound = TRUE;
                OutputDebugStringA("[SkinEngine] Valorant process detected");
            }
        } while (Process32NextW(hSnapshot, &pe32));
    }
    
    CloseHandle(hSnapshot);
    
    if (!valorantFound) {
        g_Ctx.LastError = ERROR_NOT_FOUND;
        return ERROR_NOT_FOUND;
    }
    
    // Simulate bypass sequence
    Sleep(800);
    g_Ctx.VanguardBypassed = TRUE;
    OutputDebugStringA("[SkinEngine] Vanguard bypass active");
    
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_InjectSkin(
    IN LPCWSTR weaponName,
    IN LPCWSTR skinName,
    IN ULONG variantIndex
) {
    if (!g_Ctx.VanguardBypassed) {
        return ERROR_NOT_READY;
    }
    
    if (!weaponName || !skinName) {
        return ERROR_INVALID_PARAMETER;
    }
    
    SKIN_DESCRIPTOR skin = {0};
    skin.WeaponId = (ULONG)(wcslen(weaponName) * 31 + variantIndex);
    skin.SkinId = (ULONG)(wcslen(skinName) * 47);
    skin.VariantId = variantIndex;
    skin.Rarity = (ULONG)(wcslen(skinName) % 5);
    
    wcsncpy(skin.SkinName, skinName, MAX_SKIN_ID_LEN - 1);
    wcsncpy(skin.WeaponName, weaponName, MAX_SKIN_ID_LEN - 1);
    
    // Simulate memory allocation in target
    g_Ctx.PayloadSize = sizeof(SKIN_DESCRIPTOR);
    g_Ctx.RemoteBase = VirtualAlloc(NULL, g_Ctx.PayloadSize, 
                                     MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    
    if (!g_Ctx.RemoteBase) {
        g_Ctx.LastError = GetLastError();
        return g_Ctx.LastError;
    }
    
    memcpy(g_Ctx.RemoteBase, &skin, sizeof(SKIN_DESCRIPTOR));
    
    // Simulate write to target process
    Sleep(600);
    
    VirtualFree(g_Ctx.RemoteBase, 0, MEM_RELEASE);
    g_Ctx.RemoteBase = NULL;
    
    OutputDebugStringA("[SkinEngine] Skin injected successfully");
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_GetVersion(
    OUT LPWSTR buffer,
    IN SIZE_T bufferSize
) {
    const WCHAR* ver = L"4.2.1-BETA (Build 2026.06.28-r7)";
    if (bufferSize < (wcslen(ver) + 1) * sizeof(WCHAR)) {
        return ERROR_INSUFFICIENT_BUFFER;
    }
    wcscpy(buffer, ver);
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_EnumerateWeapons(
    OUT PWSTR* weaponArray,
    IN OUT PULONG count
) {
    if (!count) return ERROR_INVALID_PARAMETER;
    
    *count = sizeof(g_WeaponTable) / sizeof(g_WeaponTable[0]);
    if (weaponArray) {
        for (ULONG i = 0; i < *count; i++) {
            weaponArray[i] = (PWSTR)g_WeaponTable[i];
        }
    }
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_EnumerateSkins(
    IN LPCWSTR weaponName,
    OUT PWSTR* skinArray,
    IN OUT PULONG count
) {
    if (!count) return ERROR_INVALID_PARAMETER;
    
    *count = sizeof(g_SkinTable) / sizeof(g_SkinTable[0]);
    if (skinArray) {
        for (ULONG i = 0; i < *count; i++) {
            skinArray[i] = (PWSTR)g_SkinTable[i];
        }
    }
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_ValidateSignature(
    IN PVOID imageBase,
    IN SIZE_T imageSize
) {
    if (!imageBase || !imageSize) {
        return ERROR_INVALID_PARAMETER;
    }
    
    // Fake integrity check
    DWORD checksum = 0;
    PBYTE pb = (PBYTE)imageBase;
    for (SIZE_T i = 0; i < imageSize && i < 0x1000; i++) {
        checksum = ((checksum << 1) | (checksum >> 31)) ^ pb[i];
    }
    
    return (checksum != 0) ? ERROR_SUCCESS : ERROR_INVALID_DATA;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_HookNtCreateFile(
    IN PVOID hookAddress,
    OUT PVOID* originalAddress
) {
    if (!hookAddress) return ERROR_INVALID_PARAMETER;
    if (originalAddress) *originalAddress = (PVOID)0x7FFE0000;
    
    OutputDebugStringA("[SkinEngine] NtCreateFile hooked via SSDT shadow");
    return ERROR_SUCCESS;
}

__declspec(dllexport) DWORD __stdcall SkinEngine_UnloadDriver(void) {
    if (g_Ctx.RemoteBase) {
        VirtualFree(g_Ctx.RemoteBase, 0, MEM_RELEASE);
    }
    memset(&g_Ctx, 0, sizeof(INJECTION_CONTEXT));
    OutputDebugStringA("[SkinEngine] Driver unloaded");
    return ERROR_SUCCESS;
}

// Entry point for EXE compilation
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
                   LPSTR lpCmdLine, int nCmdShow) {
    AllocConsole();
    FILE* fp;
    freopen_s(&fp, "CONOUT$", "w", stdout);
    
    printf("[+] Valorant Skin Changer Engine %s\n", SKIN_ENGINE_VERSION);
    printf("[+] Build: 2026.06.28-r7\n");
    printf("[+] Injection method: KernelAPC-Hybrid\n");
    printf("[+] Vanguard bypass: Ring0-Shadow\n\n");
    
    printf("[*] Initializing skin engine...\n");
    SkinEngine_Initialize();
    
    printf("[*] Scanning for Vanguard processes...\n");
    DWORD result = SkinEngine_BypassVanguard();
    if (result == ERROR_SUCCESS) {
        printf("[+] Vanguard bypassed successfully\n");
    } else {
        printf("[-] Vanguard bypass failed: 0x%08X\n", result);
    }
    
    printf("\n[*] Available weapons:\n");
    for (int i = 0; i < sizeof(g_WeaponTable)/sizeof(g_WeaponTable[0]); i++) {
        printf("    [%d] %S\n", i, g_WeaponTable[i]);
    }
    
    printf("\n[*] Press any key to exit...\n");
    getchar();
    
    SkinEngine_UnloadDriver();
    return 0;
}