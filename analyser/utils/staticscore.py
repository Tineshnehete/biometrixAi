def score_user(data):
    score = 0  # Initialize score

    # Device Profile (Max 20 Points)
    device_info = data.get("device", [])
    if len(device_info) >= 6:
        gpu, cpu_cores, ram, os_type, screen_width, screen_height, *_ = device_info
        if "Intel" in gpu or "NVIDIA" in gpu or "AMD" in gpu:
            score += 10  # Good GPU
        if cpu_cores >= 4:
            score += 5  # Enough CPU power
        if ram >= 8:
            score += 5  # Good RAM

    # Headless Detection (Max 30 Points)
    headless_flags = [
        "headlessWebDriverIsOn", "headlessHasHeadlessUA", "headlessHasHeadlessWorkerUA",
        "headlessNoChrome", "headlessHasPermissionsBug", "headlessNoPlugins", "headlessNoMimeTypes",
        "headlessNotificationIsDenied", "headlessHasKnownBgColor", "headlessPrefersLightColor",
        "headlessUaDataIsBlank", "headlessPdfIsDisabled", "headlessNoTaskbar", "headlessHasVvpScreenRes",
        "headlessHasSwiftShader", "headlessNoWebShare", "headlessNoContentIndex", "headlessNoContactsManager",
        "headlessNoDownlinkMax", "headlessHasIframeProxy", "headlessHasHighChromeIndex",
        "headlessHasBadChromeRuntime", "headlessHasToStringProxy"
    ]
    headless_count = sum(1 for flag in headless_flags if data.get(flag, False))
    
    if headless_count == 0:
        score += 30  # Fully normal browser
    elif headless_count < 5:
        score += 15  # Slight headless traits
    else:
        score += 0  # Highly likely a bot

    # User-Agent & Browser Analysis (Max 20 Points)
    user_agent = data.get("userAgent", "").lower()
    if user_agent:
        if "mozilla" in user_agent and "chrome" in user_agent:
            score += 20  # Common browser
        elif "headless" in user_agent:
            score += 5  # Suspicious user-agent
    else:
        score += 0  # No user-agent (highly suspicious)

    # WebGL & GPU Analysis (Max 15 Points)
    if "webgl" in data and data["webgl"]:
        score += 15  # WebGL enabled (good indicator)
    elif data.get("webglCapabilities", 0) != 0:
        score += 10  # Some WebGL data present
    else:
        score += 0  # No WebGL, possible bot/emulator

    # Permission & API Access (Max 15 Points)
    granted_permissions = data.get("permGranted", [])
    if granted_permissions:
        if len(granted_permissions) >= 5:
            score += 15  # Multiple permissions granted
        elif len(granted_permissions) >= 2:
            score += 10  # Some permissions granted
        else:
            score += 5  # Minimal permissions granted
    else:
        score += 0  # No permissions granted (highly suspicious)

    # Normalize score to 100
    return min(max(score, 0), 100)