import platform  # platform-dependent
import psutil  # Cross-platform
from cpuinfo import get_cpu_info
try:
    import tensorflow as tf
except ImportError:
    tf = False

try:
    import torch
except ImportError:
    torch = False

# TODO: print numbers in human-readable format

from kiwi.tracking.context.abstract_context import RunContextProvider
from kiwi.utils.mlflow_tags import KIWI_SYSTEM_HW_CPU, KIWI_SYSTEM_HW_MEMORY, KIWI_SYSTEM_HW_DISK, \
    KIWI_SYSTEM_HW_GPU, KIWI_SYSTEM_OS


def _get_cpu_info():
    advanced_cpu_info = get_cpu_info()
    cpu_info = list()
    cpu_info.append(["CPU Model:", advanced_cpu_info["brand_raw"]])
    cpu_info.append(["# Cores (Physical):", psutil.cpu_count(False)])
    cpu_info.append(["# Cores (Logical):", psutil.cpu_count(True)])
    cpu_info.append(["CPU Max Frequency:", psutil.cpu_freq().max])

    if "arch" in advanced_cpu_info:
        cpu_info.append(["Architecture:", advanced_cpu_info["arch"]])
    if "l1_data_cache_size" in advanced_cpu_info:
        cpu_info.append(["L1 Cache Size:", advanced_cpu_info["l1_data_cache_size"]])
    if "l2_cache_size" in advanced_cpu_info:
        cpu_info.append(["L2 Cache Size:", advanced_cpu_info["l2_cache_size"]])
    if "l3_cache_size" in advanced_cpu_info:
        cpu_info.append(["L3 Cache Size:", advanced_cpu_info["l3_cache_size"]])
    return cpu_info


def _get_mem_info():
    mem_info = list()
    mem_info.append(["Memory Size:", psutil.virtual_memory().total])
    mem_info.append(["Swap Size:", psutil.swap_memory().total])
    return mem_info


def _get_disk_info():
    disk_info = list()
    disk_usage = psutil.disk_usage('.')
    disk_info.append(["Total Disk Size:", disk_usage.total])
    disk_info.append(["Used Disk Size:", disk_usage.used])
    disk_info.append(["Free Disk Size:", disk_usage.free])
    return disk_info


def _get_gpu_info():
    # TODO gputil mit provide further GPU details
    # TODO look at pytorch.cuda.device and tf.config.list.physical for more details
    gpu_info = list()
    device_num = 0
    try:
        device_num = torch.cuda.device_count() if torch else 0
    except AssertionError:
        pass
    if (device_num>0 and torch):
        # Using PyTorch
        gpu_info.append(["GPU Framework:", "PyTorch"])
        gpu_info.append(["# GPUs:", torch.cuda.device_count()])
        gpu_info.append(["GPU name:", torch.cuda.get_device_name(torch.cuda.current_device())])
    elif (tf and len(tf.test.gpu_device_name())>0):
        # Using TensorFlow
        gpu_info.append(["GPU Framework:", "TensorFlow"])
        for gpu in tf.config.list_physical_devices('GPU'):
            gpu_info.append(["GPU name:", gpu.name])
    else:
        # No GPUs being used
        gpu_info.append(["# GPUs used:", 0])
    return gpu_info


def _get_os_info():
    os_info = list()
    uname = platform.uname()
    os_info.append(["Operating System:", uname.system])
    os_info.append(["Release:", uname.release])
    os_info.append(["Hostname:", uname.node])
    os_info.append(["Architecture:", uname.machine])
    return os_info


class HardwareRunContext(RunContextProvider):

    def __init__(self):
        self._cache = {}

    @property
    def _cpu_info(self):
        if "cpu_info" not in self._cache:
            self._cache["cpu_info"] = _get_cpu_info()
        return self._cache["cpu_info"]

    @property
    def _mem_info(self):
        if "mem_info" not in self._cache:
            self._cache["mem_info"] = _get_mem_info()
        return self._cache["mem_info"]

    @property
    def _disk_info(self):
        if "disk_info" not in self._cache:
            self._cache["disk_info"] = _get_disk_info()
        return self._cache["disk_info"]

    @property
    def _gpu_info(self):
        if "gpu_info" not in self._cache:
            self._cache["gpu_info"] = _get_gpu_info()
        return self._cache["gpu_info"]

    @property
    def _os_info(self):
        if "os_info" not in self._cache:
            self._cache["os_info"] = _get_os_info()
        return self._cache["os_info"]

    def in_context(self):
        return True
        # TODO: return a proper context indicator

    def tags(self):
        return {
            KIWI_SYSTEM_HW_CPU: self._cpu_info,
            KIWI_SYSTEM_HW_MEMORY: self._mem_info,
            KIWI_SYSTEM_HW_DISK: self._disk_info,
            KIWI_SYSTEM_HW_GPU: self._gpu_info,
            KIWI_SYSTEM_OS: self._os_info
        }
