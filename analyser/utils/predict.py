def calculate_trust_score(data):
    trust_score = 100  # Start with maximum trust
    
    # 1. Headless Browser Detection (35% weight)
    headless_penalty = 0
    headless_flags = [
        data.get('headlessWebDriverIsOn', False),
        data.get('headlessHasHeadlessUA', False),
        data.get('headlessNoTaskbar', False),
        data.get('headlessNotificationIsDenied', False),
        data.get('headlessNoContentIndex', False),
        data.get('headlessNoContactsManager', False)
    ]
    headless_penalty += sum(headless_flags) * 8
    if data.get('headless'):
        headless_penalty += 15
    trust_score -= headless_penalty

    # 2. Platform Consistency Checks (25% weight)
    # OS Consistency
        # 1. OS Consistency Check (Dynamic for any OS)
    def normalize_os(os_name):
        """Normalize OS names to standardized formats"""
        os_name = os_name.lower()
        if 'windows' in os_name:
            if '10' in os_name: return 'Windows 10'
            if '11' in os_name: return 'Windows 11'
            if '8.1' in os_name: return 'Windows 8.1'
            if '8' in os_name: return 'Windows 8'
            if '7' in os_name: return 'Windows 7'
            return 'Windows'
        if 'mac' in os_name or 'os x' in os_name: return 'macOS'
        if 'linux' in os_name: return 'Linux'
        if 'android' in os_name: return 'Android'
        if 'ios' in os_name: return 'iOS'
        return os_name.title()  # Return original if unknown

    def parse_ua_os(user_agent):
        """Extract OS from User Agent"""
        ua = user_agent.lower()
        if 'windows nt 10' in ua: return 'Windows 10'
        if 'windows nt 6.3' in ua: return 'Windows 8.1'
        if 'windows nt 6.2' in ua: return 'Windows 8'
        if 'windows nt 6.1' in ua: return 'Windows 7'
        if 'macintosh' in ua: return 'macOS'
        if 'linux' in ua: return 'Linux'
        if 'android' in ua: return 'Android'
        if 'iphone' in ua: return 'iOS'
        return None

    # Get OS from different sources
    device_os = normalize_os(data.get('device', [{}])[3] if len(data.get('device', [])) > 3 else '')
    ua_os = parse_ua_os(data.get('userAgent', ''))
    reported_os = normalize_os(data.get('userAgentDevice', [''])[0])

    # Check consistency between different OS reports
    os_consistency = 0
    if ua_os and device_os:
        os_consistency += 15 if ua_os == device_os else -15
    if reported_os and device_os:
        os_consistency += 10 if reported_os == device_os else -10
    if ua_os and reported_os:
        os_consistency += 5 if ua_os == reported_os else -5

    trust_score += os_consistency

    # GPU Consistency
    gpu_brand = data.get('gpuBrand', '').lower()
    gpu_match = any(gpu_brand in gpu.lower() for gpu in data.get('gpu', []))
    trust_score += 10 if gpu_match else -10

    # 3. Browser Fingerprint Validation (20% weight)
    # Font Validation
    font_score = min(len(data.get('fontList', []) * 2), 20)
    trust_score += font_score

    # WebGL Validation
    trust_score += 15 if data.get('webglParams') else -10
    trust_score += 10 if data.get('canvas') else -5

    # 4. Behavior Analysis (15% weight)
    # Permission Analysis
    perms = data.get('permGranted', [])
    trust_score += 10 if len(perms) >= 3 else -5  # Expect some permissions
    
    # Voice Consistency
    default_voice = data.get('voicesDefault', [''])[0]
    voice_match = default_voice in data.get('voices', [])
    trust_score += 5 if voice_match else -5

    # 5. Headless Probability Scores (5% weight)
    platform_estimate = data.get('headlessPlatformEstimate', {})
    windows_prob = platform_estimate.get('Windows', 0)
    trust_score += 5 if windows_prob >= 0.9 else -5

    # 6. Apply Headless Ratings Modifier
    rating_modifier = (
        data.get('headlessLikeRating', 0) - 
        data.get('headlessStealthRating', 0)
    )
    final_score = (trust_score * 0.85) + (rating_modifier * 0.15)

    # Ensure score stays within 0-100 bounds
    return max(0, min(100, int(final_score)))

# Example usage:
# trust_score = calculate_trust_score(input_data)
# print(f"Device Trust Score: {trust_score}/100")