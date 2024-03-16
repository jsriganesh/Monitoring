import psutil
import speedtest
import json
import datetime
import platform
import uuid
import subprocess
import re
import os
import time



#===================================== Check the System Boot count
def get_system_boot_count():
    try:
        # Get the boot time of the system
        output = subprocess.check_output(["sysctl", "kern.boottime"], universal_newlines=True)
        boot_time_match = re.search(r"sec = (\d+)", output)
        if boot_time_match:
            boot_time_seconds = int(boot_time_match.group(1))
        else:
            return "Unknown"

        # Get the current time
        current_time_seconds = int(time.time())

        # Calculate the time difference in seconds
        time_difference_seconds = current_time_seconds - boot_time_seconds

        # Convert seconds to days
        days_difference = time_difference_seconds // (24 * 3600)

        return days_difference
    except subprocess.CalledProcessError:
        return "Error"

#===================================== Check the Storage
#WINDOWS
def get_disk_usage_windows():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'Windows' in partition.device:
            usage = psutil.disk_usage(partition.mountpoint)
            #return usage.total, usage.used, usage.free
            return {
                "total":"{:.2f} GB".format(usage.total / (1024 ** 3)), 
                "used":"{:.2f} GB".format(usage.used / (1024 ** 3)), 
                "free":"{:.2f} GB".format(usage.free / (1024 ** 3))
                }

#LINUX
def get_disk_usage_linux():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'Linux' in partition.device:
            usage = psutil.disk_usage(partition.mountpoint)
            #return usage.total, usage.used, usage.free
            return {
                "total":"{:.2f} GB".format(usage.total / (1024 ** 3)), 
                "used":"{:.2f} GB".format(usage.used / (1024 ** 3)), 
                "free":"{:.2f} GB".format(usage.free / (1024 ** 3))
                }

#MAC
def get_disk_usage_mac():
    st = os.statvfs('/')
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return {
        "total":"{:.2f} GB".format(total / (1024 ** 3)), 
        "used":"{:.2f} GB".format(used / (1024 ** 3)), 
        "free":"{:.2f} GB".format(free / (1024 ** 3))
        }

def get_disk_usage():
    if platform.system() == 'Darwin' : 
        return get_disk_usage_mac()
    elif platform.system() == 'Windows'  :
        return get_disk_usage_windows()
    else :
        return get_disk_usage_linux()

#===================================== Check the firewall state
def check_firewall_status_mac():
    output = subprocess.run(['defaults', 'read', '/Library/Preferences/com.apple.alf', 'globalstate'], capture_output=True, text=True)
    firewall_state = output.stdout.strip()
    if firewall_state == "0":
        return "disabled"
    elif firewall_state == "1":
        return "enabled"
    else:
        return "Unable to determine firewall status"

def check_firewall_status_windows():
    output = subprocess.run(['defaults', 'read', '/Library/Preferences/com.apple.alf', 'globalstate'], capture_output=True, text=True)
    firewall_state = output.stdout.strip()
    if firewall_state == "0":
        return "disabled"
    elif firewall_state == "1":
        return "enabled"
    else:
        return "Unable to determine firewall status"

#================================================


#===================================== Check the power source (charge in-out)
def get_power_source_mac():
    result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    for line in output:
        if 'Power' in line:
            if 'AC Power' in line:
                return "Plugged In"
            elif 'Battery Power' in line:
                return "Not Plugged In"
    return "Unknown"

def get_power_source_windows():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    if plugged:
        return "Plugged In"
    else:
        return "Not Plugged In"

def get_power_source_platform_based():
    if platform.system() == 'Darwin' : 
        return get_power_source_mac()
    else:
        return get_power_source_windows()

#===================================== Check the battery percentage
def get_battery_percentage():
    system = platform.system()
    if system == "Windows" or system == "Linux":
        battery = psutil.sensors_battery()
        if battery:
            return f"{battery.percent}%"
        else:
            return "Unknown"
    elif system == "Darwin":  # macOS
        try:
            output = subprocess.check_output(["pmset", "-g", "batt"], universal_newlines=True)
            percentage_match = re.search(r"(\d+)%", output)


            if percentage_match:
                return f"{percentage_match.group(1)}%"
            else:
                return "Unknown"

        except subprocess.CalledProcessError:
            return "Error"
    else:
        return "Unsupported"

#===================================== Get All INFO
def get_system_info():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cTime = datetime.datetime.now().time()

    # Get system running hours per day
    uptime_seconds = psutil.boot_time()
    current_time = datetime.datetime.now().timestamp()
    running_hours_per_day = (current_time - uptime_seconds) / 3600.0

    # Get RAM utilization per day
    ram_utilization = psutil.virtual_memory().percent

    # Get internet speed test
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    download_speed = st.results.download / 10**6  # Convert to Mbps
    upload_speed = st.results.upload / 10**6  # Convert to Mbps

    # Get IP address
    ip_address = psutil.net_if_addrs()['en0'][0].address  # Assuming 'en0' is the network interface

    # Get MAC address
    mac_address =  ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1]) #psutil.net_if_addrs()['en0'][0].address  # Assuming 'en0' is the network interface

    # Get OS type
    os_type =  platform.system() 
    # 'Linux' for Linux distributions
    # 'Darwin' for macOS
    # 'Windows' for Windows

    # Prepare JSON object
    system_info = {
        "date": current_date,
         "time":cTime.strftime('%H:%M:%S') ,
        "running_hours_per_day": round(running_hours_per_day, 2),
        "ram_utilization": ram_utilization,
        "download_speed": round(download_speed, 2),
        "upload_speed": round(upload_speed, 2),
        "ip_address": ip_address,
        "mac_address": mac_address,
        "os_type": os_type,
        "power_incharge_indication":get_power_source_platform_based(),
        "battery_health": get_battery_percentage(),
        "storage_utilisation":get_disk_usage(),
        "system_power_up_count":get_system_boot_count(),
        "firewall_status":check_firewall_status_mac()
    }

    return system_info

if __name__ == "__main__":
    system_info = get_system_info()
    print(json.dumps(system_info, indent=4))
