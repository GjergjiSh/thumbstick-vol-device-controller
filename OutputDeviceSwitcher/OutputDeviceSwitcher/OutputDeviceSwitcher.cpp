#include "OutputDeviceSwitcher.h"
#include <iostream>

#define VALIDADTE_HR (if (!SUCCEEDED(hr)) return -1;)

bool SetDefaultAudioPlaybackDeviceById(std::wstring device_id)
{
	IPolicyConfigVista *pPolicyConfig;
	ERole reserved = eConsole;

	HRESULT hr = CoCreateInstance(__uuidof(CPolicyConfigVistaClient), NULL, CLSCTX_ALL, __uuidof(IPolicyConfigVista), (LPVOID *)&pPolicyConfig);

	if (SUCCEEDED(hr))
	{
		hr = pPolicyConfig->SetDefaultEndpoint(device_id.c_str(), reserved);
		pPolicyConfig->Release();
	}

	return SUCCEEDED(hr);
}

bool SetDefaultAudioPlaybackDeviceByIndex(UINT device_index)
{
	HRESULT hr = CoInitialize(NULL);
	bool result = false;

	if (SUCCEEDED(hr))
	{
		IMMDeviceEnumerator *pEnum = NULL;

		hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL, CLSCTX_ALL, __uuidof(IMMDeviceEnumerator), (void **)&pEnum);

		if (SUCCEEDED(hr))
		{
			IMMDeviceCollection *pDevices;

			hr = pEnum->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &pDevices);

			if (SUCCEEDED(hr))
			{
				UINT count;

				pDevices->GetCount(&count);

				if (SUCCEEDED(hr))
				{
					if (device_index >= 0 && device_index < count)
					{
						IMMDevice *pDevice;
						hr = pDevices->Item(device_index, &pDevice);

						if (SUCCEEDED(hr))
						{
							LPWSTR wstrID = NULL;

							hr = pDevice->GetId(&wstrID);

							if (SUCCEEDED(hr))
							{
								IPropertyStore *pStore;
								hr = pDevice->OpenPropertyStore(STGM_READ, &pStore);

								if (SUCCEEDED(hr))
								{
									PROPVARIANT friendlyName;

									PropVariantInit(&friendlyName);
									hr = pStore->GetValue(PKEY_Device_FriendlyName, &friendlyName);

									if (SUCCEEDED(hr))
									{
										SetDefaultAudioPlaybackDeviceById(wstrID);
										PropVariantClear(&friendlyName);

										result = true;
									}

									pStore->Release();
								}
							}

							pDevice->Release();
						}
					}
				}

				pDevices->Release();
			}

			pEnum->Release();
		}
	}

	return result;
}

// void EnumerateAudioPlaybackDevices()
// {
// 	HRESULT hr = CoInitialize(NULL);

// 	if (SUCCEEDED(hr))
// 	{
// 		IMMDeviceEnumerator *pEnum = NULL;

// 		hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL, CLSCTX_ALL, __uuidof(IMMDeviceEnumerator), (void **)&pEnum);

// 		if (SUCCEEDED(hr))
// 		{
// 			LPWSTR defaultDeviceId = NULL;
// 			IMMDevice *pDefaultDevice;

// 			HRESULT hr = pEnum->GetDefaultAudioEndpoint(eRender, eMultimedia, &pDefaultDevice);

// 			if (SUCCEEDED(hr))
// 			{
// 				hr = pDefaultDevice->GetId(&defaultDeviceId);

// 				if (!SUCCEEDED(hr))
// 				{
// 					defaultDeviceId = NULL;
// 				}

// 				pDefaultDevice->Release();
// 			}

// 			IMMDeviceCollection *pDevices;

// 			hr = pEnum->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &pDevices);

// 			if (SUCCEEDED(hr))
// 			{
// 				UINT count;

// 				pDevices->GetCount(&count);

// 				if (SUCCEEDED(hr))
// 				{
// 					for (UINT i = 0; i < count; ++i)
// 					{
// 						IMMDevice *pDevice;
// 						HRESULT hr = pDevices->Item(i, &pDevice);

// 						if (SUCCEEDED(hr))
// 						{

// 							hr = pDevice->GetId(&wstrID);

// 							if (SUCCEEDED(hr))
// 							{
// 								IPropertyStore *pStore;
// 								hr = pDevice->OpenPropertyStore(STGM_READ, &pStore);

// 								if (SUCCEEDED(hr))
// 								{
// 									PROPVARIANT friendlyName;

// 									PropVariantInit(&friendlyName);
// 									hr = pStore->GetValue(PKEY_Device_FriendlyName, &friendlyName);

// 									if (SUCCEEDED(hr))
// 									{
// 										BOOL isDefault = wcscmp(wstrID, defaultDeviceId) == 0;

// 										printf("%i %ws\n", isDefault, friendlyName.pwszVal);
// 										PropVariantClear(&friendlyName);
// 									}

// 									pStore->Release();
// 								}
// 							}

// 							pDevice->Release();
// 						}
// 					}
// 				}

// 				pDevices->Release();
// 			}

// 			pEnum->Release();
// 		}
// 	}
// }

int Init()
{
	hr = CoInitialize(NULL);
	if (!SUCCEEDED(hr))
		return -1;

	hr = CoCreateInstance(__uuidof(MMDeviceEnumerator),
						  NULL,
						  CLSCTX_ALL,
						  __uuidof(IMMDeviceEnumerator),
						  (void **)&pEnum);
	if (!SUCCEEDED(hr))
		return -1;

	if (RefreshDevicesState() != 0)
		return -1;

	return 0;
}

int RefreshDevicesState()
{
	hr = pEnum->GetDefaultAudioEndpoint(eRender,
										eMultimedia,
										&pDefaultDevice);
	if (!SUCCEEDED(hr))
		return -1;

	hr = pDefaultDevice->GetId(&defaultDeviceId);
	if (!SUCCEEDED(hr))
		defaultDeviceId = NULL;

	hr = pEnum->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &pDevices);
	if (!SUCCEEDED(hr))
		return -1;

	return 0;
}

void Deinit()
{
	pDefaultDevice->Release();
	pDevices->Release();
	pEnum->Release();
}

int GetAudioDeviceCount()
{
	// if (RefreshDevicesState() != 0)
	// 	return -1;

	UINT count;
	pDevices->GetCount(&count);

	return count;
}

int ListAudioDevices()
{
	// if (RefreshDevicesState() != 0)
	// 	return -1;

	int count = GetAudioDeviceCount();
	if (count == -1)
		return -1;

	IMMDevice *pDevice;
	IPropertyStore *pStore;
	PROPVARIANT friendlyName;
	BOOL isDefault;
	LPWSTR wstrID; //= NULL;

	for (int i = 0; i < count; i++)
	{
		hr = pDevices->Item(i, &pDevice);
		if (!SUCCEEDED(hr))
			return -1;

		hr = pDevice->GetId(&wstrID);
		if (!SUCCEEDED(hr))
			return -1;

		hr = pDevice->OpenPropertyStore(STGM_READ, &pStore);
		if (!SUCCEEDED(hr))
			return -1;
		
		PropVariantInit(&friendlyName);
		hr = pStore->GetValue(PKEY_Device_FriendlyName, &friendlyName);
		if (!SUCCEEDED(hr))
			return -1;

		isDefault = wcscmp(wstrID, defaultDeviceId) == 0;
		printf("%i %ws\n", isDefault, friendlyName.pwszVal);
		PropVariantClear(&friendlyName);
	}

	pStore->Release();
	pDevice->Release();
	return 0;
}

// bool SetDefaultAudioPlaybackDeviceByIndex(UINT device_index)
// {
// 	UINT count = GetAudioDeviceCount();
// 	if (count == -1)
// 		return false;

// 	if (device_index >= 0 && device_index < count)
// 	{
// 		IMMDevice *pDevice;
// 		HRESULT hr = pDevices->Item(device_index, &pDevice);

// 		if (SUCCEEDED(hr))
// 		{
// 			LPWSTR wstrID = NULL;

// 			hr = pDevice->GetId(&wstrID);

// 			if (SUCCEEDED(hr))
// 			{
// 				IPropertyStore *pStore;
// 				hr = pDevice->OpenPropertyStore(STGM_READ, &pStore);

// 				if (SUCCEEDED(hr))
// 				{
// 					PROPVARIANT friendlyName;

// 					PropVariantInit(&friendlyName);
// 					hr = pStore->GetValue(PKEY_Device_FriendlyName, &friendlyName);

// 					if (SUCCEEDED(hr))
// 					{
// 						SetDefaultAudioPlaybackDeviceById(wstrID);
// 						PropVariantClear(&friendlyName);
// 					}

// 					pStore->Release();
// 				}
// 			}

// 			pDevice->Release();
// 		}
// 	}

// 	return true;
// }