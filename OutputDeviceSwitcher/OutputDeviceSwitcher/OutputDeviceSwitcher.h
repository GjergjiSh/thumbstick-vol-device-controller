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

//std::vector<WindowsAudioPlaybackDevice> devices;

HRESULT hr;
IMMDeviceEnumerator *pEnum = NULL;
LPWSTR defaultDeviceId = NULL;
IMMDevice *pDefaultDevice = NULL;
IMMDeviceCollection *pDevices = NULL;

extern "C" {

	__declspec(dllexport) struct WindowsAudioPlaybackDevice
	{
		std::wstring id;
		std::wstring name;
		BOOL is_default;
	};

	typedef void (*ProcessAudioPlaybackDeviceCallback)(LPWSTR, LPWSTR, BOOL);

	__declspec(dllexport) bool SetDefaultAudioPlaybackDeviceById(std::wstring devID);
	__declspec(dllexport) bool SetDefaultAudioPlaybackDeviceByIndex(UINT device_index);
	//__declspec(dllexport) void EnumerateAudioPlaybackDevices();
	__declspec(dllexport) int GetAudioDeviceCount();
	__declspec(dllexport) int Init();
	__declspec(dllexport) int RefreshDevicesState();
	__declspec(dllexport) void Deinit();
	__declspec(dllexport) int ListAudioDevices();
}

//std::vector<WindowsAudioPlaybackDevice> GetAudioPlaybackDevices();

