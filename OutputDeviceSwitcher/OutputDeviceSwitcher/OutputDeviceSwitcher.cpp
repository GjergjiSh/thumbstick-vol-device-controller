#include "OutputDeviceSwitcher.h"

int Set_Output_Device_By_Id(std::wstring device_id)
{
	IPolicyConfigVista *policy_config;
	ERole reserved = eConsole;

	//COCREATEINSTANCE CALLED AGAIN MIGHT NEED TO REFRESH DEVICES AFTERALL
	if (!SUCCEEDED(CoCreateInstance(__uuidof(CPolicyConfigVistaClient), 
									NULL, 
									CLSCTX_ALL, 
									__uuidof(IPolicyConfigVista), 
									(LPVOID *)&policy_config)))
		return -1;

	if (!SUCCEEDED(policy_config->SetDefaultEndpoint(device_id.c_str(), reserved)))
		return -1;

	policy_config->Release();
	return 0;
}

int Init()
{
	_CrtSetReportMode(_CRT_ASSERT, 0);
	if (!SUCCEEDED(CoInitialize(NULL)))
		return -1;

	if (!SUCCEEDED(CoCreateInstance(__uuidof(MMDeviceEnumerator),
						  NULL,
						  CLSCTX_ALL,
						  __uuidof(IMMDeviceEnumerator),
						  (void **)&device_enumerator)))
		return -1;

	if (Refresh_Output_Devices_State() != 0)
		return -1;

	return 0;
}

int Refresh_Output_Devices_State()
{
	if (!SUCCEEDED(device_enumerator->GetDefaultAudioEndpoint(eRender,
										eMultimedia,
										&default_device)))
		return -1;

	if (!SUCCEEDED(default_device->GetId(&default_device_id)))
		default_device_id = NULL;

	if (!SUCCEEDED(device_enumerator->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &device_collection)))
		return -1;

	Get_Output_Device_Count();

	return 0;
}

void Deinit()
{
	default_device->Release();
	device_collection->Release();
	device_enumerator->Release();
}

int Get_Output_Device_Count()
{
	device_collection->GetCount(&device_count);
	return device_count;
}

int List_Output_Devices()
{
	if (device_count == -1)
		return -1;

	IMMDevice *device;
	IPropertyStore *property_store;
	PROPVARIANT device_name;
	BOOL is_default;
	LPWSTR device_id;

	for (int i = 0; i < device_count; i++)
	{
		if (!SUCCEEDED(device_collection->Item(i, &device)))
			return -1;

		if (!SUCCEEDED(device->GetId(&device_id)))
			return -1;

		if (!SUCCEEDED(device->OpenPropertyStore(STGM_READ, &property_store)))
			return -1;
		
		PropVariantInit(&device_name);
		if (!SUCCEEDED(property_store->GetValue(PKEY_Device_FriendlyName, &device_name)))
			return -1;

		is_default = wcscmp(device_id, default_device_id) == 0;
		printf("%i %ws\n", is_default, device_name.pwszVal);
		PropVariantClear(&device_name);
	}

	property_store->Release();
	device->Release();
	return 0;
}

int Set_Output_Device_By_Index(int device_index)
{
	if (device_count == -1)
		return -1;

	if (device_index >= 0 && device_index < device_count)
	{
		IMMDevice *device;
		if (!SUCCEEDED(device_collection->Item(device_index, &device)))
			return -1;

		LPWSTR device_id = NULL;
		printf("%i", device_id);
		auto res = device->GetId(&device_id);
		if (!SUCCEEDED(res))
			return -1;

		return Set_Output_Device_By_Id(device_id);
	}

	return -1;
}

void Print_Device_Name(UINT device_index)
{
	IMMDevice *device = NULL;
	IPropertyStore *property_store = NULL;
	LPWSTR device_id = NULL;
	PROPVARIANT device_name;

	if (device_index >= 0 && device_index < device_count)
	{
		if (!SUCCEEDED(device_collection->Item(device_index, &device)))
			return;

		if (!SUCCEEDED(device->GetId(&device_id)))
			return;

		if (!SUCCEEDED(device->OpenPropertyStore(STGM_READ, &property_store)))
			return;
		
		PropVariantInit(&device_name);
		if (!SUCCEEDED(property_store->GetValue(PKEY_Device_FriendlyName, &device_name)))
			return;
		
		std::wstring ws(device_name.pwszVal); 
		std::string result = std::string( ws.begin(), ws.end() );
		printf("Device ID: %i Device Name %s", device_index, result);
	}
}

int Get_Active_Device_Id() {
	if (device_count == -1)
		return -1;

	IMMDevice *device;
	IPropertyStore *property_store;
	BOOL is_default;
	LPWSTR device_id;

	for (int i = 0; i < device_count; i++)
	{
		if (!SUCCEEDED(device_collection->Item(i, &device)))
			return -1;

		if (!SUCCEEDED(device->GetId(&device_id)))
			return -1;

		is_default = wcscmp(device_id, default_device_id) == 0;
		if (is_default) {
			return i;
		}
	}

	property_store->Release();
	device->Release();
	return -1;
}

int Export_Device_Config() {
	if (device_count == -1)
		return -1;

	IMMDevice *device;
	IPropertyStore *property_store;
	PROPVARIANT device_name;
	BOOL is_default;
	LPWSTR device_id;
	std::ofstream config_file;

	config_file.open("./config");


	for (int i = 0; i < device_count; i++)
	{
		if (!SUCCEEDED(device_collection->Item(i, &device)))
			return -1;

		if (!SUCCEEDED(device->GetId(&device_id)))
			return -1;

		if (!SUCCEEDED(device->OpenPropertyStore(STGM_READ, &property_store)))
			return -1;
		
		PropVariantInit(&device_name);
		if (!SUCCEEDED(property_store->GetValue(PKEY_Device_FriendlyName, &device_name)))
			return -1;

		is_default = wcscmp(device_id, default_device_id) == 0;
		printf("%i %ws\n", is_default, device_name.pwszVal);
		std::wstring ws(device_name.pwszVal); 
		std::string result = std::string( ws.begin(), ws.end());
		config_file << result << "\n";
		PropVariantClear(&device_name);
	}


	config_file.close();
	property_store->Release();
	device->Release();
	return 0;
}