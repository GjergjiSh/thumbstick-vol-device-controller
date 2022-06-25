#pragma once

#include <stdio.h>
#include <wchar.h>
#include <tchar.h>
#include <vector>
#include <string>

#include "windows.h"
#include "Mmdeviceapi.h"
#include "PolicyConfig.h"
#include "Propidl.h"
#include "Functiondiscoverykeys_devpkey.h"

IMMDeviceEnumerator *device_enumerator = NULL;
LPWSTR default_device_id = NULL;
IMMDevice *default_device = NULL;
IMMDeviceCollection *device_collection = NULL;

extern "C" {

	__declspec(dllexport) struct WindowsAudioPlaybackDevice
	{
		std::wstring id;
		std::wstring name;
		BOOL is_default;
	};

	typedef void (*ProcessAudioPlaybackDeviceCallback)(LPWSTR, LPWSTR, BOOL);

	__declspec(dllexport) int Init();
	__declspec(dllexport) int Set_Output_Device_By_Id(std::wstring device_id);
	__declspec(dllexport) int Set_Output_Device_By_Index(UINT device_index);
	__declspec(dllexport) int Get_Output_Device_Count();
	__declspec(dllexport) int Refresh_Output_Devices_State();
	__declspec(dllexport) int List_Output_Devices();
	__declspec(dllexport) void Deinit();
}


