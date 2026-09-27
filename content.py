"""
content.py
All lesson content for CyberLearn, organized into tracks -> chapters -> lessons.

Design notes for contributors (this file is meant to be easy to extend on
GitHub):
  - Each lesson is ~1 minute of reading + one multiple-choice check.
  - Content here is defensive-education / conceptual-awareness material:
    how networks, defenses, and threats work, and how the security industry
    is organized -- the same level of detail taught in intro courses like
    CompTIA Security+, Network+, and any "Intro to Cybersecurity" class.
    It deliberately does not include live exploit code or step-by-step
    instructions for attacking systems you don't own or have written
    permission to test. That keeps the app genuinely useful for learning
    and safe to publish and share.
  - To add a lesson: copy an existing `L(...)` call in the relevant chapter
    and change the fields. IDs must stay unique across the whole file.
  - To add a whole new chapter or track: follow the existing structure in
    TRACKS at the bottom of this file.
"""

from __future__ import annotations
from typing import List, Dict, Any

LESSON_XP = 10


def L(lid: str, title: str, minute: str, question: str,
      choices: List[str], correct: int, explain: str) -> Dict[str, Any]:
    """Build one lesson record.

    lid       -- unique lesson id, e.g. "net_01_04"
    title     -- short lesson title shown on the path
    minute    -- the ~1 minute explanation shown before the quiz
    question  -- the single check-for-understanding question
    choices   -- list of answer options (2-4)
    correct   -- index into choices of the correct answer
    explain   -- shown after answering, reinforces the concept either way
    """
    return {
        "id": lid,
        "title": title,
        "minute": minute.strip(),
        "question": question.strip(),
        "choices": choices,
        "correct": correct,
        "explain": explain.strip(),
        "xp": LESSON_XP,
    }


def C(cid: str, title: str, lessons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build one chapter record: a titled group of lessons."""
    return {"id": cid, "title": title, "lessons": lessons}


# ---------------------------------------------------------------------------
# TRACK: NETWORKING  (foundations everything else builds on)
# ---------------------------------------------------------------------------
NETWORKING_CHAPTERS = [
    C("net_basics", "Networking Basics", [
        L("net_01_01", "What Is a Network?",
          "A network is just two or more devices that can exchange data. "
          "The internet is a network of networks: your laptop talks to a "
          "router, the router talks to your ISP, and your ISP talks to "
          "thousands of other networks worldwide. Every device that talks "
          "on a network needs a unique address so replies know where to go.",
          "What is the internet, structurally?",
          ["A single giant computer", "A network of many interconnected networks",
           "A type of website", "A government database"], 1,
          "The internet is literally 'inter-network' -- a mesh of independently "
          "run networks agreeing to pass traffic to each other."),
        L("net_01_02", "IP Addresses",
          "An IP address is a device's numeric address on a network, like "
          "192.168.1.10 (IPv4) or 2001:db8::1 (IPv6). IPv4 has ~4.3 billion "
          "addresses, which sounds like a lot until you remember every phone, "
          "laptop, and smart fridge needs one -- which is why IPv6 exists, "
          "with a vastly larger address space.",
          "Which of these is a valid IPv4 address?",
          ["192.168.1.256", "10.0.0.1", "999.1.1.1", "AB:CD:EF:01"], 1,
          "Each of the four IPv4 octets must be 0-255, so 10.0.0.1 is valid "
          "and 192.168.1.256 / 999.1.1.1 are not."),
        L("net_01_03", "Private vs Public IPs",
          "Private IP ranges (like 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12) "
          "are reusable inside any local network and aren't directly reachable "
          "from the internet. Your router uses NAT (Network Address "
          "Translation) to let every device behind it share one public IP "
          "when talking to the outside world.",
          "Why can two different homes both use the IP 192.168.1.5 without conflict?",
          ["They can't, it's always a conflict", "Private IPs are only valid inside their own local network",
           "ISPs assign it randomly", "IPv6 fixes this automatically"], 1,
          "Private address ranges are reserved for internal use only, so the "
          "same private IP can exist in millions of separate home networks."),
        L("net_01_04", "MAC Addresses",
          "A MAC address is a hardware identifier burned into a network "
          "interface, like 3C:22:FB:8A:9C:01. Unlike an IP address, it "
          "doesn't describe *where* a device is on a network -- it identifies "
          "*which* physical device it is, and is used for delivery on the "
          "local network segment (Layer 2).",
          "What layer of networking does a MAC address primarily operate at?",
          ["Application layer", "Data Link layer (Layer 2)", "Transport layer", "None, it's software only"], 1,
          "MAC addresses live at Layer 2 (Data Link) -- local delivery between "
          "devices on the same physical or virtual segment."),
    ]),
    C("net_models", "The OSI & TCP/IP Models", [
        L("net_02_01", "Why We Use Layered Models",
          "Networking is broken into layers so each piece can be built and "
          "fixed independently. Your browser doesn't need to know how Wi-Fi "
          "radio signals work, and your Wi-Fi chip doesn't need to know what "
          "HTML is -- each layer just hands data to the one below or above it.",
          "What's the main benefit of a layered network model?",
          ["It makes networks slower but safer", "Each layer can change independently without breaking the others",
           "It's required by law", "It removes the need for IP addresses"], 1,
          "Layering means innovation at one layer (like a new Wi-Fi standard) "
          "doesn't force a rewrite of everything above it."),
        L("net_02_02", "The 7 OSI Layers",
          "From bottom to top: Physical, Data Link, Network, Transport, "
          "Session, Presentation, Application. A handy mnemonic: 'Please Do "
          "Not Throw Sausage Pizza Away.' Most real troubleshooting lives at "
          "Layer 3 (routing), Layer 4 (TCP/UDP), and Layer 7 (the app itself).",
          "Which OSI layer handles routing between networks?",
          ["Layer 1 (Physical)", "Layer 3 (Network)", "Layer 5 (Session)", "Layer 7 (Application)"], 1,
          "Layer 3, the Network layer, is where IP addressing and routing "
          "decisions happen."),
        L("net_02_03", "TCP/IP: The Practical Model",
          "The real internet runs on the simpler 4-layer TCP/IP model: "
          "Link, Internet, Transport, Application. It maps roughly onto OSI "
          "but merges several layers. When people say 'Layer 7 attack' they "
          "usually mean the Application layer in this practical sense.",
          "TCP/IP's Application layer roughly corresponds to which OSI layers?",
          ["Physical + Data Link", "Session, Presentation, and Application", "Only Network", "Only Transport"], 1,
          "TCP/IP compresses OSI's top three layers (Session, Presentation, "
          "Application) into one practical Application layer."),
        L("net_02_04", "Encapsulation",
          "As data travels down the stack to be sent, each layer wraps it in "
          "its own header (and sometimes trailer) -- like nested envelopes. "
          "A web request becomes an HTTP message, wrapped in a TCP segment, "
          "wrapped in an IP packet, wrapped in an Ethernet frame.",
          "What is 'encapsulation' in networking?",
          ["Encrypting all traffic", "Wrapping data with a new header at each layer as it's sent",
           "Compressing data to save bandwidth", "Blocking unauthorized packets"], 1,
          "Encapsulation is the nesting of protocol headers, one per layer, "
          "so each layer's job stays isolated from the others."),
    ]),
    C("net_protocols", "Protocols You Must Know", [
        L("net_03_01", "TCP vs UDP",
          "TCP is connection-oriented and reliable: it handshakes, confirms "
          "delivery, and resends lost data -- great for web pages and file "
          "transfers. UDP is connectionless and fast, with no delivery "
          "guarantee -- great for video calls and gaming where speed beats "
          "perfection.",
          "Which protocol would a live video call most likely prefer, and why?",
          ["TCP, because reliability matters most", "UDP, because low latency matters more than perfect delivery",
           "Neither, video calls don't use IP", "TCP, because it's encrypted by default"], 1,
          "Video/voice favors UDP: a dropped frame is fine, but waiting for "
          "TCP retransmission causes noticeable lag."),
        L("net_03_02", "The TCP Handshake",
          "TCP connections start with a three-way handshake: SYN (client "
          "says hello), SYN-ACK (server replies and acknowledges), ACK "
          "(client confirms). Only after this does real data start flowing. "
          "This handshake is also why SYN floods are a classic DoS technique.",
          "How many steps are in the standard TCP handshake?",
          ["1", "2", "3", "4"], 2,
          "SYN, SYN-ACK, ACK -- three steps before real application data "
          "is exchanged."),
        L("net_03_03", "DNS: The Internet's Phonebook",
          "DNS (Domain Name System) translates human-friendly names like "
          "example.com into IP addresses computers actually route traffic "
          "to. Without DNS you'd have to memorize numbers for every website "
          "you visit.",
          "What does DNS primarily do?",
          ["Encrypts web traffic", "Translates domain names into IP addresses",
           "Assigns MAC addresses", "Blocks malware"], 1,
          "DNS resolution is the lookup step that turns a name into the "
          "address needed to actually connect."),
        L("net_03_04", "DHCP: Automatic Addressing",
          "DHCP (Dynamic Host Configuration Protocol) automatically hands "
          "out IP addresses, subnet masks, gateways, and DNS servers to "
          "devices joining a network -- so you don't have to configure "
          "every laptop and phone by hand.",
          "What problem does DHCP solve?",
          ["Manually configuring IP settings on every device", "Encrypting Wi-Fi traffic",
           "Routing between continents", "Translating domain names"], 0,
          "DHCP automates address assignment, which is why your phone 'just "
          "works' on a new Wi-Fi network."),
        L("net_03_05", "ARP: Finding the Physical Address",
          "ARP (Address Resolution Protocol) maps a known IP address to the "
          "MAC address needed for local delivery. When your laptop knows a "
          "peer's IP but not its MAC, it broadcasts 'who has this IP?' and "
          "the owner replies with its MAC address.",
          "What does ARP translate?",
          ["Domain names to IP addresses", "IP addresses to MAC addresses",
           "MAC addresses to domain names", "Ports to services"], 1,
          "ARP bridges Layer 3 (IP) and Layer 2 (MAC) so frames can actually "
          "be delivered on the local segment."),
    ]),
    C("net_ports", "Ports & Services", [
        L("net_04_01", "What Is a Port?",
          "A port is a number (0-65535) that identifies which service on a "
          "device a connection is meant for. An IP address gets you to the "
          "right computer; a port gets you to the right *application* on "
          "that computer.",
          "If an IP address is like a street address, a port is most like...",
          ["The country", "A specific apartment number within the building", "The postal service itself", "A password"], 1,
          "Same building (IP), different apartment (port) -- multiple "
          "services can run on one machine, each on its own port."),
        L("net_04_02", "Well-Known Ports",
          "Some ports are standardized: 80 (HTTP), 443 (HTTPS), 22 (SSH), "
          "21 (FTP), 25 (SMTP), 53 (DNS). Ports 0-1023 are 'well-known' and "
          "reserved for common services, which is why seeing port 443 open "
          "immediately tells you 'there's probably a web server here.'",
          "Which port is standard for HTTPS traffic?",
          ["21", "80", "443", "3389"], 2,
          "443 is the reserved, standard port for HTTPS (encrypted web "
          "traffic)."),
        L("net_04_03", "Open, Closed, and Filtered Ports",
          "A port scan generally reports three states: open (something's "
          "listening and responding), closed (reachable but nothing's "
          "listening), or filtered (a firewall is silently dropping probes "
          "so you can't even tell). Security teams monitor for unexpected "
          "open ports as a sign of misconfiguration or compromise.",
          "What does a 'filtered' port usually indicate?",
          ["The service crashed", "A firewall is blocking or dropping the probe", "The port doesn't exist", "The device is offline"], 1,
          "Filtered means a firewall or ACL is interfering with the probe, "
          "rather than the host directly answering open or closed."),
        L("net_04_04", "Why Minimizing Open Ports Matters",
          "Every open port is a potential entry point. Good security "
          "practice (and a core Blue Team habit) is to close or firewall "
          "off anything not explicitly needed -- this is called reducing "
          "'attack surface.'",
          "What security principle does closing unused ports follow?",
          ["Security through obscurity", "Reducing attack surface", "Defense in depth only", "Zero trust networking"], 1,
          "Fewer exposed services means fewer possible ways in -- that's "
          "attack surface reduction, one of the most cost-effective "
          "defenses that exists."),
    ]),
    C("net_devices", "Routers, Switches & Firewalls", [
        L("net_05_01", "Switches vs Routers",
          "A switch connects devices *within* the same local network and "
          "forwards traffic based on MAC address. A router connects "
          "*different* networks together (like your home network to the "
          "internet) and forwards traffic based on IP address.",
          "Which device forwards traffic between two different networks?",
          ["Switch", "Router", "Hub", "Modem"], 1,
          "Routers operate at Layer 3 and make forwarding decisions between "
          "separate networks; switches operate within one network."),
        L("net_05_02", "What a Firewall Actually Does",
          "A firewall inspects traffic and allows or blocks it based on "
          "rules -- by port, IP, protocol, or increasingly by application "
          "behavior. Think of it as a bouncer checking a guest list at every "
          "door, not a wall that blocks everything.",
          "What best describes a firewall's job?",
          ["Encrypting all network traffic", "Filtering traffic based on defined rules",
           "Speeding up internet connections", "Assigning IP addresses"], 1,
          "Firewalls filter -- they don't encrypt, and they don't speed "
          "anything up. Rule-based allow/deny is the core function."),
        L("net_05_03", "Network Segmentation",
          "Segmentation splits a network into smaller isolated zones (like "
          "putting guest Wi-Fi, IoT devices, and servers on separate VLANs) "
          "so a compromise in one zone can't freely spread to the others. "
          "It's one of the highest-leverage Blue Team defenses.",
          "Why do organizations segment their networks?",
          ["To make Wi-Fi passwords longer", "To limit how far an attacker can move if one zone is compromised",
           "To reduce their internet bill", "It's only for large ISPs"], 1,
          "Segmentation contains breaches -- an attacker on the guest Wi-Fi "
          "shouldn't have a clear path to your finance servers."),
        L("net_05_04", "VPNs, Simply",
          "A VPN (Virtual Private Network) creates an encrypted tunnel "
          "between your device and a VPN server, so traffic inside that "
          "tunnel can't be read by anyone in between -- useful on untrusted "
          "networks like public Wi-Fi, and for remote access into a private "
          "company network.",
          "What is the core security benefit a VPN provides?",
          ["It makes your internet faster", "It encrypts traffic between you and the VPN server",
           "It blocks all malware automatically", "It hides your device from your own ISP's router"], 1,
          "A VPN's job is confidentiality in transit -- an encrypted tunnel "
          "so intermediaries can't read your traffic."),
    ]),
    C("net_wireless", "Wireless & Network Security Basics", [
        L("net_06_01", "Wi-Fi Security Standards",
          "WEP is broken and should never be used. WPA2 has been standard "
          "for years. WPA3 is the current best practice, adding stronger "
          "encryption and protection against offline password-guessing "
          "attacks.",
          "Which Wi-Fi security standard should be avoided as insecure today?",
          ["WPA3", "WPA2", "WEP", "802.1X"], 2,
          "WEP's encryption was broken long ago and can be cracked quickly "
          "with widely available tools -- it should never be used."),
        L("net_06_02", "Evil Twin Awareness",
          "An 'evil twin' is a rogue Wi-Fi access point set up to mimic a "
          "legitimate one (like 'Airport_Free_WiFi'), tricking devices into "
          "connecting so the attacker can see or manipulate their traffic. "
          "Using a VPN on public Wi-Fi defends against this even if you "
          "connect to the wrong network.",
          "What is an 'evil twin' in a Wi-Fi context?",
          ["A backup router", "A rogue access point impersonating a legitimate one",
           "A type of firewall", "A second antenna on your router"], 1,
          "It mimics a trusted network's name to lure victims into "
          "connecting to an attacker-controlled access point."),
        L("net_06_03", "The CIA Triad, Applied to Networks",
          "Confidentiality (only the right people can read data), "
          "Integrity (data isn't tampered with), Availability (systems stay "
          "up when needed) -- every network security control maps back to "
          "protecting one or more of these three.",
          "Encrypting Wi-Fi traffic primarily protects which part of the CIA triad?",
          ["Availability", "Confidentiality", "Accountability", "Authenticity only"], 1,
          "Encryption's main job is keeping data unreadable to eavesdroppers "
          "-- that's confidentiality."),
        L("net_06_04", "Network Track Recap",
          "You now know how devices get addresses, how layered protocols "
          "move data, how ports identify services, how routers/switches/"
          "firewalls shape traffic flow, and the basics of wireless risk. "
          "This is the foundation every other track builds on.",
          "Which concept ties directly into almost every other security topic you'll learn next?",
          ["Font rendering", "IP addressing, ports, and traffic flow", "Color theory", "File compression"], 1,
          "Nearly every attack, defense, and tool in this app references "
          "IPs, ports, or protocols -- that's why Networking comes first."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: BLUE TEAM (defense)
# ---------------------------------------------------------------------------
BLUE_TEAM_CHAPTERS = [
    C("blue_mindset", "Defensive Mindset & the CIA Triad", [
        L("blue_01_01", "What Blue Team Means",
          "'Blue Team' refers to the defenders: the people who monitor, "
          "detect, respond to, and prevent attacks against their own "
          "organization. Where Red Team simulates the attacker, Blue Team "
          "builds and runs the actual defenses, every single day.",
          "What is the primary role of a Blue Team?",
          ["Attacking other companies", "Defending and monitoring their own organization's systems",
           "Writing marketing content", "Selling software licenses"], 1,
          "Blue Teams are defenders -- detection, response, hardening, and "
          "monitoring are their daily work."),
        L("blue_01_02", "Confidentiality",
          "Confidentiality means only authorized people or systems can "
          "access data. Encryption, access controls, and least-privilege "
          "permissions all exist primarily to protect confidentiality.",
          "Which control most directly protects confidentiality?",
          ["Backups", "Encryption and access controls", "Uptime monitoring", "Load balancing"], 1,
          "Encryption and tightly scoped access controls are the classic "
          "confidentiality controls."),
        L("blue_01_03", "Integrity",
          "Integrity means data hasn't been altered without authorization. "
          "Hashing (like SHA-256) lets you verify a file hasn't been "
          "tampered with; digital signatures extend that to proving *who* "
          "created or approved something.",
          "What technique is commonly used to verify data hasn't been tampered with?",
          ["Cryptographic hashing", "Firewalling", "Load balancing", "DNS caching"], 0,
          "A hash changes completely if even one bit of the data changes, "
          "making it a reliable tamper-detection tool."),
        L("blue_01_04", "Availability",
          "Availability means systems and data are accessible when "
          "legitimate users need them. Redundancy, backups, and DDoS "
          "protection all target availability -- it's why 'the site is "
          "just slow' is still a security incident, not just an ops one.",
          "A DDoS attack primarily threatens which part of the CIA triad?",
          ["Confidentiality", "Integrity", "Availability", "Authentication"], 2,
          "A DDoS attack floods a system so legitimate users can't use it "
          "-- a direct hit on availability."),
    ]),
    C("blue_monitoring", "Monitoring & Logging", [
        L("blue_02_01", "Why Logs Matter",
          "Logs are the record of what happened on a system: logins, file "
          "access, process launches, network connections. Without logs, "
          "investigating an incident is close to guessing. 'If it isn't "
          "logged, it didn't happen' is a common Blue Team saying.",
          "Why are logs considered critical for defense?",
          ["They make systems run faster", "They provide the evidence needed to detect and investigate incidents",
           "They're required for Wi-Fi to work", "They replace the need for firewalls"], 1,
          "Logs are the raw evidence defenders rely on to notice something "
          "happened and reconstruct what occurred."),
        L("blue_02_02", "Centralized Logging",
          "In a real environment, logs from hundreds of servers, laptops, "
          "and network devices are shipped to one central system rather "
          "than left scattered -- because an attacker who compromises one "
          "machine will often try to delete its local logs to cover their "
          "tracks.",
          "Why centralize logs instead of leaving them only on each device?",
          ["It's cheaper", "An attacker who compromises a device can delete local logs to hide evidence",
           "Centralizing improves Wi-Fi speed", "It's a legal requirement everywhere"], 1,
          "Centralized, write-once logging survives even if the attacker "
          "wipes logs on the machine they compromised."),
        L("blue_02_03", "SIEM, in Plain English",
          "A SIEM (Security Information and Event Management) system "
          "collects logs from across an organization and correlates them, "
          "flagging patterns a human would take forever to spot manually -- "
          "like the same account failing login on ten servers within a minute.",
          "What is the main job of a SIEM?",
          ["Encrypting network traffic", "Aggregating and correlating logs to surface suspicious patterns",
           "Physically securing server rooms", "Managing employee payroll"], 1,
          "A SIEM's value is correlation at scale -- connecting dots across "
          "thousands of log sources that a human couldn't watch manually."),
        L("blue_02_04", "Baselines and Anomalies",
          "You can't spot 'weird' without first knowing 'normal.' Blue "
          "Teams build a baseline of typical behavior (usual login times, "
          "typical data transfer volumes) so that deviations -- a 3am login "
          "from a new country -- stand out as worth investigating.",
          "What must exist before an 'anomaly' can be meaningfully detected?",
          ["A firewall", "A baseline of normal behavior", "A VPN", "A strong password policy"], 1,
          "Anomaly detection is inherently comparative -- you need a "
          "baseline of 'normal' before 'abnormal' means anything."),
    ]),
    C("blue_detection", "Detection: IDS, IPS & Alerts", [
        L("blue_03_01", "IDS vs IPS",
          "An IDS (Intrusion Detection System) watches traffic and alerts "
          "on suspicious activity but doesn't block it. An IPS (Intrusion "
          "Prevention System) sits inline and can actively block traffic it "
          "flags as malicious in real time.",
          "What's the key difference between an IDS and an IPS?",
          ["IDS blocks traffic, IPS only alerts", "IDS only alerts, IPS can actively block traffic",
           "They are the same thing", "IPS only works on Wi-Fi"], 1,
          "IDS = detect and alert. IPS = detect and actively intervene. The "
          "'P' is for Prevention."),
        L("blue_03_02", "Signature-Based Detection",
          "Signature-based detection matches traffic or files against known "
          "patterns of malicious activity, similar to antivirus definitions. "
          "It's fast and low false-positive, but blind to brand-new, unseen "
          "(zero-day) threats.",
          "What is a limitation of purely signature-based detection?",
          ["It's too slow to be useful", "It can't detect entirely new, previously unseen threats",
           "It only works on Windows", "It requires no maintenance ever"], 1,
          "If a threat has no known signature yet, signature-based tools "
          "simply won't recognize it -- this is why behavioral detection "
          "exists too."),
        L("blue_03_03", "Behavioral / Anomaly-Based Detection",
          "Instead of matching known bad patterns, behavioral detection "
          "flags activity that deviates from a baseline -- like a user "
          "account suddenly downloading gigabytes of data at 2am. It can "
          "catch novel attacks, at the cost of more false positives to tune.",
          "What kind of threat is behavioral detection better positioned to catch than pure signature matching?",
          ["Only viruses from the 1990s", "Novel or previously unseen attack patterns", "Only phishing emails", "Hardware failures"], 1,
          "Because it doesn't rely on a known signature, behavioral "
          "detection can flag genuinely new attack patterns."),
        L("blue_03_04", "Alert Fatigue",
          "A SOC (Security Operations Center) that gets thousands of low "
          "quality alerts a day will start missing the real ones -- this is "
          "'alert fatigue,' and tuning detection rules to reduce noise is a "
          "constant, unglamorous part of real Blue Team work.",
          "What is 'alert fatigue'?",
          ["A hardware malfunction", "Analysts missing real threats because they're overwhelmed by low-quality alerts",
           "A type of malware", "A firewall setting"], 1,
          "Too much noise drowns out the signal -- well-tuned detection is "
          "as important as having detection at all."),
    ]),
    C("blue_ir", "Incident Response Basics", [
        L("blue_04_01", "The IR Lifecycle",
          "A widely taught incident response cycle: Preparation, "
          "Identification, Containment, Eradication, Recovery, Lessons "
          "Learned. Skipping 'Lessons Learned' is one of the most common "
          "real-world mistakes -- teams fix the fire and never ask why it started.",
          "Which phase comes right after 'Identification' in standard incident response?",
          ["Recovery", "Containment", "Lessons Learned", "Preparation"], 1,
          "After identifying an incident, the priority is Containment -- "
          "stop it from spreading before eradicating it."),
        L("blue_04_02", "Containment Strategies",
          "Containment isolates the problem: disconnecting an infected "
          "machine from the network, disabling a compromised account, or "
          "blocking a malicious IP -- fast, decisive moves to stop the "
          "bleeding before full cleanup begins.",
          "What is the primary goal of the containment phase?",
          ["Fully repair all damage", "Stop the incident from spreading further", "Write the final report",
           "Interview all employees"], 1,
          "Containment is about stopping the spread quickly -- deep cleanup "
          "and repair come in the later Eradication and Recovery phases."),
        L("blue_04_03", "Chain of Custody",
          "When evidence (logs, disk images, memory dumps) might matter "
          "later -- for HR, legal, or law enforcement -- responders "
          "document exactly who handled it, when, and how, so its integrity "
          "can be trusted later. This is 'chain of custody.'",
          "Why does chain of custody matter during incident response?",
          ["It's just paperwork with no real value", "It preserves evidence integrity so it can be trusted later, including legally",
           "It speeds up containment", "It replaces the need for logs"], 1,
          "Without documented chain of custody, evidence can be challenged "
          "as unreliable or tampered with later on."),
        L("blue_04_04", "Post-Incident Review",
          "After the fire is out, mature teams run a blameless "
          "post-incident review: what happened, what worked, what didn't, "
          "and what changes will prevent a repeat. 'Blameless' matters -- "
          "people hide information when they fear punishment.",
          "Why do mature IR teams favor 'blameless' post-incident reviews?",
          ["To avoid ever fixing problems", "So people share honest details instead of hiding mistakes out of fear",
           "Because blame is illegal", "It's required by every insurance policy"], 1,
          "Fear of blame makes people withhold details -- a blameless "
          "culture gets more honest, useful information out on the table."),
    ]),
    C("blue_hardening", "Hardening Systems", [
        L("blue_05_01", "What 'Hardening' Means",
          "Hardening is the process of reducing a system's attack surface: "
          "disabling unused services, applying patches, enforcing strong "
          "configurations, and removing default credentials. It's "
          "unglamorous, and it prevents more incidents than almost anything else.",
          "What does 'hardening' a system generally involve?",
          ["Adding more open ports", "Reducing attack surface via patching, disabling unused services, and secure config",
           "Installing more software regardless of need", "Ignoring default passwords"], 1,
          "Hardening shrinks the number of ways in -- patch, disable, "
          "restrict, and remove anything unnecessary."),
        L("blue_05_02", "Patch Management",
          "Unpatched software is one of the single biggest causes of real "
          "world breaches -- attackers reuse known, already-fixed "
          "vulnerabilities because so many organizations are slow to apply "
          "updates. A disciplined patch cycle is one of the highest-ROI "
          "defenses that exists.",
          "Why do attackers frequently target known, already-patched vulnerabilities?",
          ["Patched vulnerabilities are actually more dangerous", "Many organizations are slow to apply available patches, leaving them exposed",
           "Patches always introduce new vulnerabilities", "It's illegal to patch quickly"], 1,
          "Patches exist; the gap is in how quickly organizations apply "
          "them -- attackers exploit that lag."),
        L("blue_05_03", "Least Privilege",
          "The principle of least privilege means every account, process, "
          "or user gets only the access strictly necessary to do their job "
          "-- nothing more. If an account is compromised, least privilege "
          "limits the blast radius of what the attacker can actually do.",
          "What does the principle of least privilege reduce?",
          ["The speed of the network", "The potential damage if an account or process is compromised",
           "The number of employees needed", "The cost of hardware"], 1,
          "Limiting access limits impact -- a compromised low-privilege "
          "account simply can't do as much damage."),
        L("blue_05_04", "Default Credentials",
          "Countless breaches trace back to devices left with factory "
          "default usernames/passwords (admin/admin is a classic). Changing "
          "defaults on every device -- routers, cameras, IoT gear -- is one "
          "of the simplest, cheapest defenses available.",
          "Why are default credentials a serious risk?",
          ["They're always too complex to remember", "They're publicly documented and attackers check for them automatically",
           "They only affect old hardware", "They improve device performance"], 1,
          "Default creds are published in manuals and scanned for "
          "automatically -- leaving them unchanged is an open door."),
    ]),
    C("blue_crypto", "Cryptography Fundamentals", [
        L("blue_06_01", "Encryption vs Hashing",
          "Encryption is reversible: you encrypt data, and with the right "
          "key you can decrypt it back. Hashing is one-way: you can't "
          "reverse a hash back into the original data. That's exactly why "
          "passwords are hashed, not encrypted, for storage.",
          "Why are passwords typically hashed rather than encrypted for storage?",
          ["Hashing is faster to compute", "Hashing is one-way, so even the storing system can't recover the original password",
           "Encryption doesn't exist for text", "Hashing uses less disk space"], 1,
          "Storing a one-way hash means even a full database breach doesn't "
          "directly hand over plaintext passwords."),
        L("blue_06_02", "Symmetric vs Asymmetric Encryption",
          "Symmetric encryption uses one shared key for both encrypting and "
          "decrypting (fast, but you must securely share the key). "
          "Asymmetric encryption uses a public/private key pair -- anyone "
          "can encrypt with your public key, but only your private key can "
          "decrypt it.",
          "What is the key advantage of asymmetric encryption over symmetric?",
          ["It's always faster", "It avoids needing to securely pre-share a single secret key",
           "It doesn't require any keys at all", "It's only used for video streaming"], 1,
          "Asymmetric encryption solves the 'how do we securely share a "
          "key in the first place' problem that pure symmetric encryption has."),
        L("blue_06_03", "TLS/HTTPS in Ten Seconds",
          "HTTPS wraps HTTP in TLS: a handshake negotiates a shared session "
          "key (often using asymmetric crypto), then all traffic for that "
          "session is encrypted symmetrically, which is much faster for "
          "bulk data. That padlock icon means confidentiality and integrity "
          "in transit.",
          "What does the padlock icon in a browser's address bar primarily indicate?",
          ["The website has no bugs", "The connection to that specific site is encrypted via TLS",
           "The website is guaranteed trustworthy content", "The site has no ads"], 1,
          "The padlock confirms an encrypted TLS connection -- it says "
          "nothing about whether the site's *content* is trustworthy."),
        L("blue_06_04", "Salting Passwords",
          "A 'salt' is random data added to a password before hashing, "
          "unique per user. It defeats precomputed 'rainbow table' attacks "
          "and ensures two users with the same password get completely "
          "different stored hashes.",
          "What problem does salting a password hash solve?",
          ["It makes hashing reversible", "It defeats precomputed lookup-table attacks and hides identical passwords",
           "It speeds up login", "It removes the need for hashing entirely"], 1,
          "Without a salt, identical passwords produce identical hashes, "
          "and attackers can use massive precomputed tables to crack them "
          "instantly -- salting breaks that shortcut."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: RED TEAM (offense, conceptual & ethical -- authorized testing only)
# ---------------------------------------------------------------------------
RED_TEAM_CHAPTERS = [
    C("red_intro", "What Red Teaming Actually Is", [
        L("red_01_01", "Red Team, Defined",
          "A Red Team simulates real adversary techniques against an "
          "organization -- with written authorization -- to find weaknesses "
          "before real attackers do. Every engagement starts with a signed "
          "scope: what's in bounds, what's off-limits, and who to call if "
          "something goes wrong.",
          "What must exist before any legitimate Red Team engagement begins?",
          ["Nothing, it's fine to just start testing", "Written authorization defining scope and rules of engagement",
           "A press release", "A public vote"], 1,
          "Testing systems without explicit written authorization isn't Red "
          "Teaming -- it's a crime. Scope and authorization come first, always."),
        L("red_01_02", "Rules of Engagement",
          "Rules of Engagement (RoE) spell out exactly what's allowed: "
          "which IP ranges, what techniques are off-limits (like actually "
          "disrupting production), testing windows, and emergency contacts. "
          "Staying inside RoE is what separates a professional tester from "
          "someone committing a crime.",
          "What is the purpose of Rules of Engagement in a security assessment?",
          ["To make the test harder", "To clearly define legal, agreed-upon testing boundaries",
           "To slow down the report", "They're optional paperwork"], 1,
          "RoE is the legal and practical boundary of the engagement -- "
          "operating outside it is unauthorized access, full stop."),
        L("red_01_03", "Red Team vs Penetration Test",
          "A penetration test usually targets a defined system over a set "
          "time to find as many vulnerabilities as possible. A Red Team "
          "engagement is broader and stealthier -- testing whether the "
          "Blue Team can detect and respond to a realistic, goal-driven "
          "adversary, not just cataloguing bugs.",
          "What's a key difference between a pentest and a Red Team engagement?",
          ["They are identical", "Red Team also tests detection and response, not just finding vulnerabilities",
           "Pentests are always illegal", "Red Team never has a scope"], 1,
          "Pentesting asks 'what's broken?' Red Teaming also asks 'would we "
          "notice and stop a real attacker?'"),
        L("red_01_04", "Purple Teaming",
          "'Purple Team' isn't a separate group -- it's Red and Blue "
          "actively collaborating, sharing what techniques were used and "
          "what defenders saw (or missed), in real time, to improve "
          "detection faster than a report-and-wait model allows.",
          "What is the goal of 'Purple Teaming'?",
          ["Replacing the Blue Team entirely", "Red and Blue collaborating directly to improve detection faster",
           "A cheaper version of Red Teaming with no value", "Only used for marketing"], 1,
          "Purple Teaming closes the feedback loop -- attackers and "
          "defenders working together beats a one-way report."),
    ]),
    C("red_recon", "Reconnaissance Concepts", [
        L("red_02_01", "Passive vs Active Recon",
          "Passive recon gathers information without touching the target "
          "directly -- public records, DNS history, job postings, social "
          "media. Active recon interacts with the target directly, like "
          "sending scan packets, which is noisier and easier to detect.",
          "What distinguishes passive recon from active recon?",
          ["Passive recon is illegal, active is legal", "Passive recon never directly touches the target; active recon does",
           "There's no real difference", "Passive recon only works on weekends"], 1,
          "Passive recon stays 'outside the fence' using public sources; "
          "active recon sends traffic directly at the target."),
        L("red_02_02", "OSINT",
          "OSINT (Open-Source Intelligence) is information gathered from "
          "publicly available sources: company websites, LinkedIn, DNS "
          "records, code repositories, leaked-but-public breach data. "
          "Defenders use OSINT too -- to see what an attacker would "
          "already know about them.",
          "OSINT relies on what kind of sources?",
          ["Only classified government data", "Publicly available, open sources", "Only paid dark web access", "Only internal company documents"], 1,
          "OSINT is explicitly about *open* sources -- nothing here "
          "requires breaking in to obtain."),
        L("red_02_03", "Attack Surface Mapping",
          "Before testing anything, a tester maps what's actually exposed: "
          "domains, subdomains, IP ranges, cloud assets, and public-facing "
          "applications. You can't test -- or defend -- what you don't know "
          "exists, which is why 'shadow IT' (forgotten, unmanaged systems) "
          "is such a common real-world risk.",
          "Why is 'shadow IT' a significant security risk?",
          ["It's always faster than sanctioned IT", "It creates unmanaged, often unpatched systems that defenders don't even know to monitor",
           "It's a marketing term with no real risk", "It only affects small companies"], 1,
          "You can't secure what security teams don't know exists -- "
          "unmanaged shadow systems are blind spots by definition."),
        L("red_02_04", "Social Engineering Recon",
          "Attackers (and authorized testers, with consent) research "
          "employees to craft convincing pretexts -- names, roles, "
          "reporting lines, even out-of-office replies leak useful timing "
          "information. This is why oversharing on public profiles is a "
          "real organizational risk, not just a personal one.",
          "Why might an out-of-office auto-reply be useful recon for a social engineer?",
          ["It never contains useful information", "It can reveal who's away, for how long, and who's covering for them",
           "It automatically grants system access", "It's always disabled by default"], 1,
          "Small details like 'I'm out until Monday, contact Jamie in my "
          "absence' hand an attacker exact timing and a name to impersonate "
          "or target."),
    ]),
    C("red_scanenum", "Scanning & Enumeration Concepts", [
        L("red_03_01", "Scanning vs Enumeration",
          "Scanning finds what's *there*: which hosts are alive, which "
          "ports are open. Enumeration digs deeper into what scanning "
          "found: what service and version is actually running on that "
          "open port, and what it might expose.",
          "What is the difference between scanning and enumeration?",
          ["They're the same step", "Scanning finds what exists; enumeration extracts detail about what was found",
           "Enumeration always comes before scanning", "Scanning is illegal, enumeration is legal"], 1,
          "Scanning is breadth-first discovery; enumeration is the "
          "depth-first follow-up on each discovery."),
        L("red_03_02", "Service Banners & Fingerprinting",
          "Many services announce their own name and version in a "
          "'banner' when you connect -- which helps testers (and attackers) "
          "identify exactly what software is running, and check it against "
          "known vulnerabilities. This is why hiding or minimizing banners "
          "is a small but real hardening step.",
          "What can a service banner reveal to someone scanning a network?",
          ["Nothing useful", "The service name and version, useful for identifying known vulnerabilities",
           "The administrator's password", "The company's revenue"], 1,
          "A banner like 'OpenSSH 7.2' tells a tester exactly what to check "
          "against known vulnerability databases for that specific version."),
        L("red_03_03", "Vulnerability Scanning",
          "Automated vulnerability scanners compare discovered services and "
          "versions against databases of known weaknesses (like CVE "
          "listings), producing a prioritized list for a human to verify -- "
          "they're a starting point, not a substitute for expert analysis.",
          "What is the role of an automated vulnerability scanner?",
          ["To replace human testers entirely", "To flag known potential weaknesses for a human to verify and prioritize",
           "To automatically fix every issue found", "To encrypt company data"], 1,
          "Scanners triage at scale, but confirming real impact and "
          "eliminating false positives still needs a skilled analyst."),
        L("red_03_04", "False Positives",
          "Not every flagged finding is real -- automated tools "
          "misidentify things constantly. A core skill in offensive "
          "security is manually validating findings before they ever go "
          "into a client report, so time isn't wasted chasing ghosts.",
          "Why is manual validation important after an automated scan?",
          ["Automated scans are always 100% accurate", "Scanners can produce false positives that waste time if reported unverified",
           "Validation is only needed for low severity findings", "It's purely a formality with no real value"], 1,
          "A report full of unverified false positives destroys trust and "
          "wastes the client's remediation effort -- validation is essential."),
    ]),
    C("red_vulns", "Common Vulnerability Classes", [
        L("red_04_01", "Injection Flaws, Conceptually",
          "Injection vulnerabilities happen when untrusted input is "
          "interpreted as code or commands instead of pure data -- SQL "
          "injection being the classic example, where unsanitized input "
          "changes the meaning of a database query. The fix is always the "
          "same idea: never trust input, and use parameterized queries.",
          "What is the root cause behind most injection vulnerabilities?",
          ["Slow servers", "Untrusted input being interpreted as executable code or commands instead of plain data",
           "Weak Wi-Fi passwords", "Outdated fonts"], 1,
          "Injection flaws all share one root cause: input that should be "
          "inert data instead gets interpreted and executed."),
        L("red_04_02", "Broken Access Control",
          "This is when a system fails to properly enforce what a user is "
          "allowed to do -- like a regular user editing a URL's ID "
          "parameter and viewing someone else's private data. It's "
          "consistently one of the most common real-world web vulnerability "
          "classes.",
          "What does 'broken access control' generally allow an attacker to do?",
          ["Nothing of concern", "Access or modify data/functions they shouldn't be authorized to reach",
           "Only slow down a website", "Change the website's color scheme"], 1,
          "It's a failure to enforce permission boundaries -- users end up "
          "able to reach data or actions outside their authorization."),
        L("red_04_03", "Misconfiguration",
          "Not every vulnerability is a coding bug -- default settings left "
          "unchanged, unnecessary debug modes left enabled, or overly "
          "permissive cloud storage settings are all misconfigurations, and "
          "collectively they're one of the most common findings in real "
          "assessments.",
          "What category of issue is 'leaving cloud storage publicly readable by mistake'?",
          ["A network cable issue", "A security misconfiguration", "A hardware failure", "A DNS problem"], 1,
          "Misconfiguration is about incorrect settings, not flawed code -- "
          "and it's extremely common because defaults are often insecure."),
        L("red_04_04", "Outdated Components",
          "Using software libraries or components with known, publicly "
          "documented vulnerabilities is one of the most preventable "
          "vulnerability classes -- the fix (usually just updating) already "
          "exists, but inventory and patching gaps let old, exploitable "
          "versions linger.",
          "Why is 'using components with known vulnerabilities' considered especially preventable?",
          ["Because the fix is unknown", "Because a fix or update usually already exists and just needs applying",
           "Because it's always intentional", "Because it can't be detected"], 1,
          "Unlike a zero-day, a known vulnerability already has a public "
          "fix -- the failure is usually in inventory and patch management, "
          "not in some unsolvable technical problem."),
    ]),
    C("red_exploit", "Exploitation Concepts", [
        L("red_05_01", "What 'Exploitation' Means",
          "Exploitation is using a discovered weakness to actually "
          "demonstrate impact -- proving a vulnerability is real and "
          "significant, not just theoretical. In authorized testing this is "
          "done carefully, in scope, and often with safeguards to avoid "
          "disrupting production systems.",
          "In professional security testing, what is the purpose of exploitation?",
          ["To cause maximum damage for fun", "To demonstrate real-world impact of a vulnerability, safely and within scope",
           "It serves no purpose", "To permanently delete client data"], 1,
          "The goal is proof of impact for the client's benefit, done "
          "carefully within agreed boundaries -- not destruction."),
        L("red_05_02", "Proof of Concept vs Weaponization",
          "A proof of concept (PoC) demonstrates a vulnerability exists "
          "with minimal, controlled impact. 'Weaponizing' turns that into a "
          "fully automated, repeatable attack tool -- which is exactly why "
          "responsible researchers are careful about what technical detail "
          "they publish and when.",
          "What is the key difference between a PoC and a weaponized exploit?",
          ["They're the same thing", "A PoC minimally demonstrates the issue; weaponized tools are built for repeatable, automated attack",
           "PoCs are always illegal", "Weaponized tools are always safer"], 1,
          "A PoC proves the point exists; weaponization is building it into "
          "a tool optimized for repeated, scaled attack -- a meaningfully "
          "different and riskier thing to publish."),
        L("red_05_03", "Post-Exploitation Goals",
          "After gaining initial access in an authorized test, the next "
          "questions are usually: can I escalate privileges? can I move to "
          "other systems? what sensitive data is reachable? These "
          "questions show a client the real business impact, not just 'a "
          "box was popped.'",
          "Why do testers explore post-exploitation impact rather than stopping at initial access?",
          ["It's just for bragging rights", "It demonstrates the real business impact a breach could have, which drives remediation priority",
           "It's required by every law globally", "Initial access is never useful information"], 1,
          "Business impact -- what data or systems are actually reachable -- "
          "is what gets a vulnerability prioritized and fixed, not just its "
          "existence on paper."),
        L("red_05_04", "Staying Legal and Ethical",
          "Every technique in this track is only legitimate with explicit, "
          "written authorization from the system owner. The same skills "
          "used against consenting clients are federal crimes when used "
          "against systems you don't have permission to test -- the "
          "authorization is what defines the entire profession.",
          "What single factor separates legitimate security testing from a crime, given the exact same technical skill?",
          ["The attacker's intelligence", "Explicit, documented authorization from the system's owner", "The time of day", "The operating system used"], 1,
          "Authorization is the entire line -- identical techniques are "
          "either a paid, legal engagement or a serious crime, depending "
          "only on whether the owner said yes in writing."),
    ]),
    C("red_reporting", "Reporting & Communicating Findings", [
        L("red_06_01", "Why the Report Is the Deliverable",
          "In professional offensive security, the report -- not the "
          "exploit -- is the actual product a client pays for. A brilliant "
          "finding that's poorly explained and doesn't get fixed helped no one.",
          "What is generally considered the real deliverable of a security assessment?",
          ["The exploit code itself", "A clear report that drives real remediation", "A verbal summary only", "Nothing, testing is the whole point"], 1,
          "Clients pay to get *more secure*, not to watch a demo -- the "
          "report is what actually drives that outcome."),
        L("red_06_02", "Severity Ratings",
          "Findings are typically rated (e.g. Critical/High/Medium/Low) "
          "based on both technical severity and business impact, often "
          "using a scoring framework like CVSS, so a client with limited "
          "time and budget knows exactly what to fix first.",
          "Why do reports assign severity ratings to findings?",
          ["To make the report longer", "To help the client prioritize limited remediation time and budget",
           "It's purely cosmetic", "Ratings are randomly assigned"], 1,
          "Not everything can be fixed at once -- severity ratings tell the "
          "client where to spend their limited remediation effort first."),
        L("red_06_03", "Reproducibility",
          "A good finding write-up includes exact, step-by-step "
          "reproduction details so the client's engineers can verify the "
          "issue themselves and confirm the fix later -- vague findings "
          "('something about login') waste everyone's time.",
          "Why does a finding need clear, step-by-step reproduction steps?",
          ["So the client's engineers can verify and later confirm the fix", "It's only for the tester's personal notes",
           "Reproduction steps are never needed", "To make the report look impressive"], 0,
          "Without reproducible steps, the client's team can't confirm the "
          "issue is real or later confirm it's actually fixed."),
        L("red_06_04", "Red Team Track Recap",
          "You've covered the full lifecycle: authorization and scope, "
          "recon, scanning and enumeration, common vulnerability classes, "
          "exploitation concepts, and reporting. Every step exists inside a "
          "legal, authorized framework -- that framework is the whole "
          "profession.",
          "What is the thread connecting every stage of a Red Team engagement?",
          ["Speed above all else", "Operating within explicit authorization and a defined scope", "Avoiding all documentation", "Working entirely alone"], 1,
          "Authorization and scope aren't a footnote to Red Teaming -- "
          "they're the foundation everything else is built on."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: WHITE HAT (ethics, legality, and career)
# ---------------------------------------------------------------------------
WHITE_HAT_CHAPTERS = [
    C("white_ethics", "Ethics & the Law", [
        L("white_01_01", "The Hat Spectrum",
          "'White hat' describes security professionals who work with "
          "authorization to improve security. 'Black hat' describes those "
          "who attack systems illegally, without consent, for personal "
          "gain or harm. 'Grey hat' sits uncomfortably in between -- acting "
          "without authorization but claiming good intent, which is still "
          "illegal in most places.",
          "What fundamentally distinguishes 'white hat' from 'black hat' activity?",
          ["The programming language used", "Authorization -- white hat always has explicit permission", "White hats work for free", "Black hats only target banks"], 1,
          "It's not the technique that defines the hat -- it's whether the "
          "system owner authorized the activity."),
        L("white_01_02", "Computer Fraud Laws, Generally",
          "Most countries have laws (like the CFAA in the U.S., or the "
          "Computer Misuse Act in the UK) that make accessing a computer "
          "system without authorization a crime -- regardless of whether "
          "any damage occurred or the intent was 'just looking around.'",
          "Under laws like the CFAA, what generally makes unauthorized access illegal?",
          ["Only if data is deleted", "The unauthorized access itself, regardless of intent or damage", "Only if money changes hands", "Only if it happens across country borders"], 1,
          "Unauthorized access is typically illegal on its own -- 'I didn't "
          "damage anything' is not a legal defense."),
        L("white_01_03", "Consent Is Not Implied",
          "A company having a public website doesn't mean testing it is "
          "authorized. A bug bounty program's scope document, or a signed "
          "contract, is what grants permission -- and only for exactly what "
          "it covers.",
          "Does a publicly accessible website imply permission to security-test it?",
          ["Yes, anything public can be tested freely", "No -- explicit authorization or a defined bug bounty scope is required",
           "Only on weekends", "Only if you don't get caught"], 1,
          "Public accessibility is not the same as authorization -- testing "
          "requires explicit permission, typically a signed scope or bounty "
          "program terms."),
        L("white_01_04", "Why Ethics Matter Beyond the Law",
          "Even where something might be technically legal, professional "
          "ethics go further: minimizing harm, respecting privacy, "
          "disclosing responsibly, and not exploiting findings for personal "
          "gain. Reputation in this field is built over years and lost in "
          "one bad decision.",
          "Why do security professionals hold themselves to standards beyond just 'what's legal'?",
          ["Ethics have no practical value", "To minimize harm and maintain the trust the profession depends on",
           "Because clients never notice the difference", "Ethics are only relevant to government work"], 1,
          "Trust is the currency of this field -- ethical practice protects "
          "both the people affected and the tester's own career."),
    ]),
    C("white_disclosure", "Responsible Disclosure", [
        L("white_02_01", "What Responsible Disclosure Means",
          "When a researcher finds a vulnerability, responsible disclosure "
          "means privately notifying the affected organization first, "
          "giving them reasonable time to fix it before any public details "
          "are released -- protecting users in the meantime.",
          "What is the core idea behind responsible disclosure?",
          ["Publish everything immediately for attention", "Privately notify the vendor first and give them time to fix it before going public",
           "Never tell anyone, ever", "Only disclose to competitors"], 1,
          "Private notice first, public details later -- giving the vendor "
          "a real chance to protect their users before attackers can "
          "exploit the same information."),
        L("white_02_02", "Coordinated Disclosure Timelines",
          "Many researchers and vendors agree on a standard window (often "
          "90 days) to fix an issue before public disclosure -- balancing "
          "the vendor's need for time against the risk of an issue staying "
          "silently unpatched forever with no pressure to act.",
          "Why do many disclosure policies use a fixed timeline (like 90 days)?",
          ["It's an arbitrary tradition with no purpose", "It balances giving the vendor time to fix the issue against the risk of indefinite inaction",
           "Longer timelines are always safer for users", "It's required by international law everywhere"], 1,
          "A deadline creates healthy pressure to actually fix the issue, "
          "while still giving the vendor reasonable time to do it properly."),
        L("white_02_03", "Safe Harbor",
          "A 'safe harbor' clause in a bug bounty or vulnerability "
          "disclosure policy is a legal promise: if you test within the "
          "stated scope and rules, the organization won't pursue legal "
          "action against you. Testing without one is meaningfully riskier.",
          "What does a 'safe harbor' clause in a disclosure policy protect a researcher from?",
          ["Nothing, it's symbolic", "Legal action from the organization, as long as the researcher stays within stated scope and rules",
           "Being paid for their work", "Having to write a report"], 1,
          "Safe harbor is the organization's written promise not to pursue "
          "legal action against good-faith research done within their "
          "stated rules."),
        L("white_02_04", "Never Access More Than Needed to Prove It",
          "A responsible researcher demonstrates a vulnerability exists "
          "with the minimum necessary access -- proving, say, that they "
          "*could* read other users' data without actually downloading or "
          "browsing it. Going further turns a finding into a violation.",
          "What's the recommended approach when proving a data-exposure vulnerability?",
          ["Download as much data as possible to prove severity", "Demonstrate access is possible with the minimum necessary proof, then stop",
           "Share the data publicly to prove it's real", "Ignore it since proving it isn't necessary"], 1,
          "Minimum necessary proof is the standard -- going beyond that "
          "point turns responsible research into an actual privacy "
          "violation."),
    ]),
    C("white_bounty", "Bug Bounty Basics", [
        L("white_03_01", "What a Bug Bounty Program Is",
          "A bug bounty program is a company's formal invitation for "
          "researchers to test their systems (within defined scope) in "
          "exchange for recognition and often payment, scaled by severity. "
          "Platforms like HackerOne and Bugcrowd host many of these programs.",
          "What does a bug bounty program formally provide to researchers?",
          ["Unlimited access to test anything, anywhere", "Explicit authorization to test within a defined scope, often with paid rewards",
           "A guaranteed job offer", "Free antivirus software"], 1,
          "It's explicit, scoped authorization plus an incentive structure "
          "-- turning what would otherwise be illegal access into a "
          "welcomed, rewarded activity."),
        L("white_03_02", "Reading Scope Carefully",
          "Every bounty program lists in-scope assets (and explicitly "
          "out-of-scope ones). Testing something outside scope -- even "
          "with good intentions -- can void safe harbor protection and "
          "cross into illegal territory.",
          "Why is carefully reading a bounty program's scope so important?",
          ["Scope is just a suggestion", "Testing outside scope can void legal protection, even if the intent was good", "All company assets are always in scope by default", "Scope only matters for large companies"], 1,
          "Safe harbor only covers what's explicitly in scope -- straying "
          "outside it removes that legal protection entirely."),
        L("white_03_03", "Duplicate and Non-Qualifying Reports",
          "Bounty programs typically pay only for the *first* valid report "
          "of a unique issue, and many exclude certain classes of low-"
          "impact findings by policy. Understanding a program's rules "
          "before submitting saves everyone time.",
          "What commonly happens to the second researcher who reports an already-known issue?",
          ["They get paid double", "The report is usually marked as a duplicate and not separately rewarded", "They're banned from the platform", "Nothing changes for anyone"], 1,
          "Most programs reward first-to-report -- which is why speed and "
          "reading existing disclosure policy both matter."),
        L("white_03_04", "Building a Reputation",
          "Consistent, high-quality, well-written reports build a "
          "researcher's reputation on bounty platforms over time -- which "
          "often matters more for long-term opportunity than any single "
          "payout.",
          "What tends to matter most for long-term success on bug bounty platforms?",
          ["A single lucky big payout", "Consistent, high-quality, clearly documented reports over time", "Submitting as many low-effort reports as possible", "Working alone and never reading policy"], 1,
          "Reputation compounds -- quality and consistency open doors "
          "(and better opportunities) that one big score usually doesn't."),
    ]),
    C("white_career", "Certifications & Career Paths", [
        L("white_04_01", "Popular Entry Certifications",
          "CompTIA Security+ is a common starting point covering broad "
          "fundamentals. From there, paths diverge: offensive-leaning "
          "certs (like OSCP) emphasize hands-on exploitation, while "
          "defensive-leaning ones (like Security+, CySA+, or vendor SIEM "
          "certs) emphasize monitoring and response.",
          "What does CompTIA Security+ typically serve as?",
          ["An advanced, offense-only credential", "A broad, foundational entry-level cybersecurity certification", "A programming language certification", "A hardware repair certification"], 1,
          "Security+ is widely used as a foundational, vendor-neutral "
          "entry point covering broad security concepts."),
        L("white_04_02", "Offensive vs Defensive Career Tracks",
          "Offensive careers (pentester, Red Teamer) focus on finding and "
          "demonstrating weaknesses. Defensive careers (SOC analyst, "
          "detection engineer, incident responder) focus on spotting and "
          "stopping real attacks. Many practitioners move between both over "
          "a career, and understanding one side deeply helps the other.",
          "Why might understanding offensive techniques help someone working a defensive role?",
          ["It has no relevance to defense", "Understanding how attacks work helps defenders recognize and detect them faster",
           "Offensive knowledge is only useful for breaking the law", "Defenders are legally barred from learning offense"], 1,
          "You defend better against what you understand -- this is exactly "
          "why Purple Teaming and cross-training between roles is so valued."),
        L("white_04_03", "Home Labs Over Credentials Alone",
          "Hands-on practice -- home labs, Capture The Flag (CTF) "
          "competitions, and platforms built for legal practice -- often "
          "matters as much to employers as certificates on paper, because "
          "it demonstrates real applied skill, not just memorized theory.",
          "What do CTF competitions and home labs primarily demonstrate to employers?",
          ["Nothing beyond a certificate already shows", "Practical, applied hands-on skill beyond memorized theory", "Only theoretical knowledge", "Typing speed"], 1,
          "Applied, hands-on demonstrated skill is often weighted as "
          "heavily as -- or more than -- certification alone."),
        L("white_04_04", "Soft Skills Matter More Than People Expect",
          "Clear writing (reports get read by non-technical executives "
          "too), calm communication during incidents, and the ability to "
          "explain risk in business terms are consistently cited as "
          "differentiators between good and great security professionals.",
          "Why do communication skills matter so much in cybersecurity roles?",
          ["They don't -- only technical skill matters", "Findings and incidents must often be explained clearly to non-technical decision-makers",
           "Only sales roles need communication skills", "Writing is never part of the job"], 1,
          "A brilliant finding that decision-makers can't understand or act "
          "on doesn't drive any actual improvement -- communication is "
          "part of the real job."),
    ]),
    C("white_lab", "Building a Home Lab Safely", [
        L("white_05_01", "Why Practice on Your Own Lab",
          "A home lab -- virtual machines running intentionally vulnerable "
          "software, isolated from the internet and your real network -- "
          "lets you practice real techniques with zero legal risk, because "
          "you own every system involved and it's fully isolated.",
          "What makes practicing on a personal, isolated home lab legally safe?",
          ["Nothing, it's still risky", "You own and control every system involved, with clear authorization by definition", "It's only safe if you don't save any files", "Home labs are illegal everywhere"], 1,
          "Ownership is authorization -- testing systems you fully own and "
          "control, isolated from others, carries no legal risk."),
        L("white_05_02", "Isolation Matters",
          "A lab environment should be network-isolated (using a "
          "hypervisor's 'host-only' or 'internal' network mode) so "
          "intentionally vulnerable practice machines, or practice malware "
          "samples, can never reach the real internet or your home network "
          "by accident.",
          "Why should a practice lab be isolated from your home network?",
          ["Isolation isn't necessary", "To prevent intentionally vulnerable systems or samples from ever affecting real, live networks", "It makes the lab run slower on purpose", "Only for legal compliance paperwork"], 1,
          "Isolation is the safety net -- it ensures a deliberately "
          "vulnerable practice machine can never become a real-world "
          "problem for you or anyone else."),
        L("white_05_03", "Legal Practice Platforms",
          "Purpose-built platforms host intentionally vulnerable "
          "applications and CTF-style challenges specifically for legal "
          "practice -- giving learners real technique practice against "
          "systems explicitly built and offered for that purpose.",
          "What do purpose-built practice platforms provide?",
          ["Illegal access to real company systems", "Intentionally vulnerable systems explicitly offered for legal, hands-on practice", "Only theoretical quizzes, no hands-on practice", "Access requires breaking a law first"], 1,
          "These platforms exist specifically to make hands-on practice "
          "legal and safe -- explicit permission is built into their "
          "purpose."),
        L("white_05_04", "White Hat Track Recap",
          "You've covered the ethical and legal foundation of the entire "
          "field: what separates the hats, responsible disclosure, bug "
          "bounties, career paths, and safe practice. This track is the "
          "one that makes every other track usable without risking your "
          "freedom or your future.",
          "Why is the White Hat track described as foundational to using every other track safely?",
          ["It isn't, it's optional trivia", "It defines the legal and ethical boundaries that make offensive skills usable without risk",
           "It only applies to certifications", "It replaces the need for authorization"], 1,
          "Skills without an ethical/legal framework are a liability -- "
          "this track is what makes the offensive knowledge in this app "
          "safe to actually hold."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: BLACK HAT AWARENESS (understanding threats to defend against them)
# ---------------------------------------------------------------------------
BLACK_HAT_CHAPTERS = [
    C("black_landscape", "The Threat Landscape", [
        L("black_01_01", "Why Study the Attacker's Playbook",
          "This track is framed defensively: understanding how real "
          "attackers think and operate is how defenders anticipate and "
          "recognize attacks -- the same reason security teams study threat "
          "intelligence reports. It is not a how-to for attacking anyone.",
          "What is the purpose of studying attacker methodology in security education?",
          ["To learn how to break the law", "To help defenders anticipate, recognize, and stop real attacks", "It has no defensive value", "Only law enforcement is allowed to study this"], 1,
          "Every major security certification includes 'know your enemy' "
          "material -- understanding attacker goals and patterns is core "
          "defensive knowledge."),
        L("black_01_02", "Threat Actor Categories",
          "Security researchers broadly categorize attackers: opportunistic "
          "cybercriminals (financially motivated), organized crime groups, "
          "nation-state actors (espionage, sabotage), hacktivists "
          "(ideologically motivated), and insider threats (someone already "
          "inside the organization).",
          "What primarily motivates a typical opportunistic cybercriminal, as opposed to a nation-state actor?",
          ["Financial gain, versus espionage or strategic advantage", "They're always identical in motivation", "Neither has any specific motivation", "Boredom only"], 0,
          "Different threat actor categories have different goals -- "
          "financial gain for cybercriminals versus strategic/espionage "
          "goals for nation-state actors -- which shapes their tactics."),
        L("black_01_03", "The Cyber Kill Chain",
          "A widely taught model describes attack stages: Reconnaissance, "
          "Weaponization, Delivery, Exploitation, Installation, Command & "
          "Control, and Actions on Objectives. Defenders try to break the "
          "chain at the earliest possible stage.",
          "Why do defenders prefer to stop an attack at an early kill chain stage rather than a late one?",
          ["Later stages are always easier to stop", "Earlier stages mean less damage has occurred and less cleanup is needed", "It makes no difference at all", "Late-stage detection is always impossible"], 1,
          "The earlier an attack is caught, the less damage and cleanup -- "
          "stopping Reconnaissance beats cleaning up after 'Actions on "
          "Objectives.'"),
        L("black_01_04", "Motive, Means, Opportunity",
          "Understanding risk means thinking about all three: does a "
          "credible actor want to target you (motive), do they have the "
          "capability (means), and does a weakness exist for them to use "
          "(opportunity)? Removing any one of the three reduces real risk.",
          "Which of the three -- motive, means, or opportunity -- is most directly under a defender's own control?",
          ["Motive", "Means", "Opportunity (reducing your own exposed weaknesses)", "None of them are controllable"], 2,
          "You generally can't control who wants to target you or their "
          "resources -- but you can directly reduce the opportunities "
          "(vulnerabilities, exposure) available to them."),
    ]),
    C("black_socialeng", "Social Engineering & Phishing Awareness", [
        L("black_02_01", "Why Humans Are Targeted",
          "Technical defenses have gotten much stronger, so attackers "
          "increasingly target the human directly -- because a convincing "
          "email is often cheaper and more reliable than finding a "
          "technical flaw. Social engineering exploits trust, urgency, and "
          "authority, not code.",
          "Why do attackers increasingly favor social engineering over purely technical attacks?",
          ["Humans are technically impossible to defend", "It's often cheaper and more reliable than finding and exploiting a technical flaw",
           "Social engineering is easier to prosecute", "It requires more technical skill than exploitation"], 1,
          "As technical defenses improve, the human element often becomes "
          "the path of least resistance -- exploiting trust rather than code."),
        L("black_02_02", "Phishing Red Flags",
          "Common warning signs: urgency ('act now or your account is "
          "locked'), mismatched sender domains, generic greetings, requests "
          "to bypass normal process, and links that don't match their "
          "displayed text when you hover over them.",
          "What is a classic red flag of a phishing email?",
          ["A calm, no-deadline tone", "Artificial urgency pressuring immediate action", "A correctly matching sender domain", "No links or attachments at all"], 1,
          "Manufactured urgency is a core social engineering tactic -- it "
          "pushes targets to act before they think carefully."),
        L("black_02_03", "Spear Phishing vs Mass Phishing",
          "Mass phishing casts a wide, generic net hoping a few percent "
          "bite. Spear phishing is personalized and researched -- using a "
          "real name, project, or colleague -- making it far more "
          "convincing and dangerous, and usually targeting specific "
          "high-value individuals.",
          "What makes spear phishing generally more dangerous than mass phishing?",
          ["It's sent to more people at once", "It's personalized and researched, making it far more convincing", "It never contains links", "It's always easier to detect"], 1,
          "Personalization is what makes spear phishing effective -- a "
          "message referencing your actual manager or project bypasses the "
          "instinct that catches generic scams."),
        L("black_02_04", "Pretexting",
          "Pretexting is inventing a believable scenario to manipulate "
          "someone -- posing as IT support needing a password reset, or a "
          "vendor needing an urgent invoice paid. Verifying requests "
          "through a separate, known-trusted channel is the standard defense.",
          "What is the recommended defense against a suspicious request, like an urgent password reset from 'IT'?",
          ["Comply immediately to be helpful", "Verify the request independently through a separate, already-trusted channel", "Ignore all IT requests forever", "Forward it to more people"], 1,
          "Out-of-band verification -- calling a known number, not one "
          "provided in the suspicious message itself -- defeats most "
          "pretexting attempts."),
    ]),
    C("black_malware", "Malware Families (Conceptual)", [
        L("black_03_01", "Virus vs Worm vs Trojan",
          "A virus attaches to and needs a host file/program to spread. A "
          "worm spreads on its own across networks without needing a host "
          "or user action. A trojan disguises itself as legitimate "
          "software to trick a user into installing it voluntarily.",
          "What is the key distinguishing trait of a worm compared to a virus?",
          ["Worms need a host file to spread; viruses don't", "Worms self-propagate across networks without needing a host file", "They are exactly the same thing", "Worms only affect mobile phones"], 1,
          "Self-propagation without needing to attach to another file or "
          "wait for user action is what defines a worm."),
        L("black_03_02", "Ransomware, Conceptually",
          "Ransomware encrypts a victim's files and demands payment for "
          "the decryption key. Modern variants often also steal data first "
          "and threaten to leak it ('double extortion'), which is why "
          "backups alone no longer fully solve the problem.",
          "Why do backups alone no longer fully protect against modern ransomware?",
          ["Backups have become illegal", "Modern ransomware often also steals and threatens to leak data, not just encrypt it", "Ransomware no longer encrypts files", "Backups are always encrypted too"], 1,
          "'Double extortion' means even a perfect backup doesn't stop the "
          "threat of stolen data being published -- prevention and "
          "detection matter as much as recovery."),
        L("black_03_03", "Spyware and Keyloggers, Conceptually",
          "Spyware covertly monitors activity -- keyloggers specifically "
          "capture keystrokes to steal credentials. Understanding that "
          "these exist, and why unique passwords plus multi-factor "
          "authentication limit their damage, is the useful defensive "
          "takeaway here.",
          "What defense meaningfully limits the damage even if a password is stolen via a keylogger?",
          ["Using the same password everywhere", "Multi-factor authentication", "Writing passwords down", "Disabling all software updates"], 1,
          "MFA means a stolen password alone isn't enough to log in -- it's "
          "one of the highest-impact defenses against credential theft."),
        L("black_03_04", "Botnets",
          "A botnet is a network of compromised devices ('bots'), often "
          "including hijacked IoT devices, controlled remotely by an "
          "attacker to launch coordinated attacks like DDoS or mass "
          "spam campaigns -- device owners are frequently unaware their "
          "hardware is part of one.",
          "What is a botnet primarily made of?",
          ["A single powerful attacker machine", "A network of many compromised devices controlled remotely", "A type of firewall", "A legitimate cloud service"], 1,
          "Scale is the point of a botnet -- thousands of hijacked devices "
          "acting together, often without their owners ever noticing."),
    ]),
    C("black_ransomware", "Ransomware & Extortion Deep Dive", [
        L("black_04_01", "Common Initial Access Points",
          "Ransomware operators commonly get in through phishing emails, "
          "exposed and poorly secured remote access (like RDP with weak "
          "passwords), or exploiting unpatched, known vulnerabilities -- "
          "unglamorous, well-known entry points, not exotic zero-days.",
          "What is a commonly abused, unglamorous entry point for ransomware attacks?",
          ["Only brand-new zero-day vulnerabilities", "Exposed remote access services with weak passwords, like RDP", "Encrypted USB drives", "Fiber optic cable taps"], 1,
          "Most ransomware incidents trace back to boring, well-known "
          "weaknesses -- phishing and weakly secured remote access -- not "
          "exotic techniques."),
        L("black_04_02", "Why Paying the Ransom Is Discouraged",
          "Law enforcement and most security professionals discourage "
          "paying: it funds further criminal operations, doesn't guarantee "
          "working decryption or that stolen data won't leak anyway, and "
          "can mark a victim as a reliable future target.",
          "What is one commonly cited reason security professionals discourage paying ransoms?",
          ["Payment always guarantees full data recovery", "It funds further criminal activity and doesn't guarantee full recovery", "It's always tax deductible", "Ransom payments are illegal to refuse"], 1,
          "Paying doesn't reliably solve the problem and directly funds the "
          "criminal ecosystem behind future attacks."),
        L("black_04_03", "The Value of Offline Backups",
          "A backup that ransomware can reach and encrypt too isn't much "
          "of a backup. Offline or immutable backups -- ones an attacker on "
          "the network genuinely cannot modify or delete -- are the "
          "difference between a bad day and a business-ending event.",
          "Why must effective ransomware-resistant backups be offline or immutable?",
          ["Online backups are always faster to restore", "A backup reachable by an attacker on the network can be encrypted or deleted too",
           "Immutable backups are always more expensive with no benefit", "It doesn't actually matter"], 1,
          "If ransomware (or the attacker) can reach and modify your "
          "backup, it stops being a reliable recovery option -- isolation "
          "is what makes a backup actually resilient."),
        L("black_04_04", "Incident Communication",
          "During a ransomware incident, clear, honest, timely "
          "communication with employees, customers, and sometimes "
          "regulators is both an ethical and often legal obligation -- "
          "silence or downplaying an incident tends to cause more lasting "
          "damage than the incident itself.",
          "Why does honest, timely communication matter during a security incident?",
          ["It's irrelevant to the outcome", "It's often a legal obligation and reduces long-term reputational damage", "Silence always protects a company's reputation better", "Only technical teams need to know"], 1,
          "Downplaying or hiding incidents tends to backfire badly once the "
          "truth emerges -- and in many jurisdictions, timely disclosure is "
          "a legal requirement, not just good practice."),
    ]),
    C("black_history", "Famous Breaches & Lessons Learned", [
        L("black_05_01", "The Common Thread in Major Breaches",
          "Looking across major publicized breaches over the years, a "
          "pattern repeats: the root cause is very often something "
          "mundane -- an unpatched known vulnerability, a phished "
          "credential, a misconfigured cloud bucket -- not an exotic, "
          "never-seen-before technique.",
          "What do many major, publicized data breaches commonly have in common at their root cause?",
          ["Exotic, never-before-seen zero-day techniques", "Mundane, well-known issues like unpatched systems or phished credentials", "They're all caused by insiders", "Weather-related outages"], 1,
          "The unglamorous truth: basic hygiene failures (patching, "
          "phishing resistance, config review) explain far more breaches "
          "than exotic novel attacks."),
        L("black_05_02", "Why Basics Beat Exotic Defenses",
          "Advanced detection tools matter, but organizations that nail "
          "the fundamentals -- patching, MFA, backups, least privilege, "
          "logging -- prevent far more incidents than those chasing "
          "cutting-edge tools while skipping the basics.",
          "What does security research consistently show prevents the most incidents?",
          ["Only the newest, most expensive tools", "Consistent execution of fundamentals like patching, MFA, and backups",
           "Avoiding all cloud services entirely", "Hiring the largest possible security team"], 1,
          "Fundamentals, done consistently, prevent more real incidents "
          "than any single advanced tool -- this is one of the most "
          "repeated lessons in the field."),
        L("black_05_03", "Supply Chain Risk",
          "Some of the most damaging incidents came through trusted "
          "third-party software or vendors being compromised first, then "
          "used as a stepping stone into many downstream victims at once -- "
          "which is why vetting vendors' security matters, not just your own.",
          "What is a 'supply chain attack' in cybersecurity?",
          ["An attack on physical shipping logistics only", "Compromising a trusted third-party vendor/software to reach many downstream victims at once", "A type of phishing email", "An outdated networking term with no modern relevance"], 1,
          "Attackers increasingly compromise one trusted supplier to reach "
          "many organizations downstream at once -- far more efficient "
          "than attacking each target directly."),
        L("black_05_04", "Black Hat Awareness Track Recap",
          "You've now covered attacker motivations, social engineering, "
          "malware types, ransomware mechanics, and lessons from real "
          "breaches -- all through a defensive lens. Understanding this "
          "side of the field makes every defense you build afterward far "
          "more targeted and effective.",
          "What is the intended defensive purpose of everything covered in this track?",
          ["To teach illegal attack techniques for personal use", "To help you recognize, anticipate, and defend against real threat patterns", "It has no practical application", "To discourage anyone from working in defense"], 1,
          "Every lesson here maps back to a defensive payoff -- recognizing "
          "patterns is how you stop them before they cause harm."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: PYTHON PROGRAMMING (the scripting skill every path benefits from)
# ---------------------------------------------------------------------------
PYTHON_CHAPTERS = [
    C("py_basics", "Python Basics", [
        L("py_01_01", "Variables & Print",
          "Python variables need no type declaration -- `name = \"Nova\"` "
          "just works. `print()` displays output to the console, and is "
          "usually the very first thing anyone runs in any language, in "
          "any tutorial, ever.",
          "What will `print(2 + 2)` output?",
          ["'2 + 2'", "4", "22", "An error"], 1,
          "Python evaluates the expression first (2 + 2 = 4), then prints "
          "the result."),
        L("py_01_02", "Core Data Types",
          "The basics: `int` (whole numbers), `float` (decimals), `str` "
          "(text, in quotes), and `bool` (True/False). Python figures out "
          "the type automatically from how you write the value.",
          "What data type is `True`?",
          ["str", "int", "bool", "float"], 2,
          "`True` and `False` are Python's boolean type, used constantly in "
          "conditions and comparisons."),
        L("py_01_03", "String Basics",
          "Strings can use single or double quotes interchangeably. "
          "f-strings (`f\"Hello {name}\"`) let you embed variables directly "
          "inside text -- the modern, preferred way to build formatted "
          "strings in Python.",
          "What does `f\"Score: {10+5}\"` evaluate to?",
          ["'Score: {10+5}'", "'Score: 15'", "An error", "'Score:'"], 1,
          "f-strings evaluate the expression inside the curly braces and "
          "insert the result directly into the string."),
        L("py_01_04", "Input from the User",
          "`input(\"prompt\")` pauses a program and waits for the user to "
          "type something, always returning it as a string -- even if they "
          "typed a number, you'd need `int(...)` to convert it.",
          "What type does `input()` always return, before any conversion?",
          ["int", "str", "bool", "It depends what the user typed"], 1,
          "`input()` always returns a string -- converting to int/float is "
          "a separate, explicit step you do afterward."),
    ]),
    C("py_control", "Control Flow", [
        L("py_02_01", "if / elif / else",
          "Conditional logic lets a program branch: `if condition:` runs "
          "one block, `elif` checks another condition, `else` catches "
          "everything else. Indentation (not braces) defines each block in "
          "Python -- this is a real, enforced part of the syntax.",
          "What defines a code block in Python, instead of curly braces?",
          ["Semicolons", "Consistent indentation", "Parentheses", "Nothing, blocks aren't a real concept"], 1,
          "Python uses indentation itself as syntax -- inconsistent "
          "indentation is actually a syntax error, not just a style issue."),
        L("py_02_02", "for Loops",
          "`for item in collection:` runs a block once per item in a list, "
          "string, or range. `for i in range(5):` runs exactly 5 times, "
          "with `i` counting 0, 1, 2, 3, 4.",
          "How many times does `for i in range(5):` execute its block?",
          ["4", "5", "6", "Infinite"], 1,
          "`range(5)` produces 0 through 4 -- five values total, so the "
          "loop body runs five times."),
        L("py_02_03", "while Loops",
          "`while condition:` repeats a block as long as the condition "
          "stays true. It's easy to accidentally write an infinite loop if "
          "you forget to update whatever the condition depends on inside "
          "the loop body.",
          "What's the most common cause of an accidental infinite `while` loop?",
          ["Using `for` instead of `while`", "Forgetting to update the variable the loop condition depends on", "Using too many print statements", "Python doesn't allow while loops"], 1,
          "If the condition's variable never changes inside the loop, the "
          "condition stays true forever and the loop never ends."),
        L("py_02_04", "break and continue",
          "`break` immediately exits a loop entirely. `continue` skips the "
          "rest of the current iteration and moves to the next one, "
          "without exiting the whole loop.",
          "What does `continue` do inside a loop?",
          ["Exits the loop completely", "Skips to the next iteration without exiting the loop", "Restarts the program", "Pauses execution forever"], 1,
          "`continue` jumps straight to the next loop iteration, skipping "
          "any remaining code for the current one -- unlike `break`, which "
          "exits entirely."),
    ]),
    C("py_functions", "Functions & Modules", [
        L("py_03_01", "Defining Functions",
          "`def name(parameters):` defines a reusable block of code. "
          "Functions let you write logic once and call it many times, "
          "which is the foundation of not repeating yourself as programs "
          "grow.",
          "What keyword starts a function definition in Python?",
          ["func", "function", "def", "define"], 2,
          "`def` is the keyword; the function body follows, indented "
          "underneath the `def` line."),
        L("py_03_02", "Return Values",
          "`return` sends a value back out of a function to wherever it "
          "was called from. A function with no `return` statement "
          "implicitly returns `None`.",
          "What does a Python function return if it has no explicit `return` statement?",
          ["0", "An empty string", "None", "It causes an error"], 2,
          "Without an explicit `return`, Python functions implicitly "
          "return `None`, not zero or an empty value."),
        L("py_03_03", "Parameters & Default Values",
          "Functions can have default parameter values: `def greet(name=\"friend\"):` "
          "lets you call `greet()` with no arguments and still get sensible "
          "behavior, or override it with `greet(\"Nova\")`.",
          "What happens if you call `greet()` where `def greet(name=\"friend\"):`?",
          ["It raises an error because no argument was given", "`name` takes the default value \"friend\"", "It always returns None", "Python requires all arguments explicitly"], 1,
          "Default parameter values are used automatically whenever the "
          "caller doesn't supply that argument."),
        L("py_03_04", "Importing Modules",
          "`import module_name` brings in code from Python's standard "
          "library (like `os`, `json`, `hashlib`) or third-party packages, "
          "so you don't have to reinvent common functionality yourself.",
          "What does `import hashlib` let you use in your program?",
          ["Functions and tools from the hashlib module", "Nothing, hashlib isn't a real module", "Only file operations", "It deletes the hashlib folder"], 0,
          "`import` loads a module so its functions and classes become "
          "available under that module's name, like `hashlib.sha256(...)`."),
    ]),
    C("py_data", "Data Structures", [
        L("py_04_01", "Lists",
          "A list (`[1, 2, 3]`) is an ordered, mutable (changeable) "
          "collection. You can append, remove, index (`my_list[0]`), and "
          "slice (`my_list[1:3]`) items freely.",
          "What does `my_list[0]` access in a list?",
          ["The last item", "The first item", "The length of the list", "A random item"], 1,
          "Python indexing starts at 0, so `[0]` is always the first "
          "element of a sequence."),
        L("py_04_02", "Dictionaries",
          "A dictionary (`{\"key\": \"value\"}`) stores key-value pairs "
          "with fast lookup by key -- perfect for structured data like "
          "`{\"name\": \"Nova\", \"role\": \"analyst\"}`.",
          "How do you retrieve the value for `\"name\"` in `d = {\"name\": \"Nova\"}`?",
          ["d[0]", "d.name", "d[\"name\"]", "d->name"], 2,
          "Dictionaries are accessed by key using square brackets, not by "
          "numeric position."),
        L("py_04_03", "Tuples",
          "A tuple (`(1, 2, 3)`) looks like a list but is immutable -- once "
          "created, it can't be changed. Useful for fixed collections of "
          "values, like coordinates, that shouldn't accidentally be modified.",
          "What is the key difference between a tuple and a list?",
          ["Tuples can hold more items", "Tuples are immutable; lists are mutable", "Lists can't be indexed", "There is no real difference"], 1,
          "Immutability is the defining trait of a tuple -- once set, its "
          "contents can't be changed, unlike a list."),
        L("py_04_04", "Sets",
          "A set (`{1, 2, 3}`) is an unordered collection of unique "
          "values -- duplicates are automatically removed. Sets are ideal "
          "for fast membership checks and de-duplicating data, like a list "
          "of unique IPs seen in a log file.",
          "What happens if you add a duplicate value to a Python set?",
          ["It's added twice", "It's ignored -- sets automatically only keep unique values", "It raises an error", "It replaces all existing items"], 1,
          "Sets enforce uniqueness automatically -- adding a value already "
          "present simply has no effect."),
    ]),
    C("py_files", "File I/O & Working with Text", [
        L("py_05_01", "Opening Files Safely",
          "`with open(\"file.txt\") as f:` is the standard, safe way to "
          "open a file -- it automatically closes the file afterward, even "
          "if an error happens partway through, which manual `open()`/`close()` "
          "doesn't guarantee.",
          "Why is `with open(...) as f:` preferred over manually calling `open()` and `close()`?",
          ["It's shorter to type only", "It automatically closes the file even if an error occurs inside the block", "It opens files faster", "It's required by Python's syntax rules"], 1,
          "The `with` statement guarantees cleanup (closing the file) "
          "happens automatically, even during an exception -- manual open/"
          "close can leak an open file handle if an error occurs first."),
        L("py_05_02", "Reading Line by Line",
          "`for line in f:` reads a file one line at a time, which is "
          "memory-efficient for large files -- you're never loading the "
          "entire file into memory at once, unlike `f.read()`.",
          "Why might `for line in f:` be preferred over `f.read()` for a huge log file?",
          ["It's always faster regardless of file size", "It processes the file line-by-line instead of loading it entirely into memory at once", "f.read() doesn't work on text files", "There's no real difference"], 1,
          "Line-by-line iteration keeps memory usage low regardless of file "
          "size -- important for genuinely large files like server logs."),
        L("py_05_03", "Writing to Files",
          "`with open(\"out.txt\", \"w\") as f: f.write(\"hello\")` writes "
          "text to a file, overwriting existing content. Using `\"a\"` "
          "instead of `\"w\"` appends to the end instead of overwriting.",
          "What happens if you open a file in `\"w\"` mode that already has content?",
          ["The new content is appended to the end", "The existing content is overwritten/erased", "Python refuses to open it", "It merges both versions automatically"], 1,
          "`\"w\"` mode truncates the file first -- if you want to keep "
          "existing content, use `\"a\"` (append) mode instead."),
        L("py_05_04", "Parsing Structured Text",
          "Real-world text (like CSV log lines) is often parsed with "
          "`.split(\",\")` or the built-in `csv` module, turning a raw line "
          "of text into structured data you can actually work with "
          "programmatically -- a common first step in log analysis scripts.",
          "What does `\"a,b,c\".split(\",\")` return?",
          ["\"abc\"", "['a', 'b', 'c']", "('a', 'b', 'c')", "An error"], 1,
          "`.split(\",\")` breaks a string into a list wherever the comma "
          "appears -- the foundation of simple CSV-style parsing."),
    ]),
    C("py_security", "Python for Security Tasks", [
        L("py_06_01", "Hashing Files in Python",
          "The built-in `hashlib` module can compute a file's SHA-256 hash "
          "-- useful for verifying a downloaded file hasn't been tampered "
          "with, by comparing against a hash the publisher provides.",
          "Which built-in Python module provides hashing functions like SHA-256?",
          ["os", "hashlib", "json", "socket"], 1,
          "`hashlib` is the standard library module for cryptographic "
          "hashing in Python -- `hashlib.sha256(data).hexdigest()` is a "
          "common pattern."),
        L("py_06_02", "Parsing Your Own Log Files",
          "A short Python script reading your own server's access log, "
          "counting requests per IP with a dictionary, is a genuinely "
          "useful, completely legal security task -- spotting an IP with "
          "an unusually high request count is a simple way to notice "
          "possible scanning or brute-force activity.",
          "What simple pattern in your own logs might suggest a brute-force attempt?",
          ["A single normal login", "An unusually high number of requests or failed logins from one source in a short time", "A request at 9am", "Any request using HTTPS"], 1,
          "A spike in failed attempts or requests from a single source is a "
          "classic, simple signal worth investigating -- easy to script "
          "with a dictionary counting occurrences per IP."),
        L("py_06_03", "Working With Your Own Local Server",
          "Python's built-in `http.server` module can spin up a local test "
          "web server in one line (`python -m http.server`) -- extremely "
          "useful for safely practicing web requests, testing scripts, or "
          "serving files on your own machine, with zero external risk.",
          "What does running `python -m http.server` do?",
          ["Deletes all files in the current folder", "Starts a simple local web server serving the current folder", "Sends spam email", "Scans the internet for open ports"], 1,
          "It's a built-in, zero-setup local web server -- perfect for "
          "safely practicing HTTP requests entirely on your own machine."),
        L("py_06_04", "Why Python Is Popular in Security",
          "Python's simple syntax, huge standard library, and thousands of "
          "security-focused third-party packages make it the most common "
          "scripting language for automating repetitive security tasks, "
          "from log parsing to report generation.",
          "What is a major reason Python is so widely used in the security field?",
          ["It's the only language that can connect to the internet", "Simple syntax plus a huge ecosystem of libraries makes automation fast to write", "It's required by law for security tools", "It runs faster than compiled languages"], 1,
          "Speed of writing and reading code, plus a massive ecosystem of "
          "existing libraries, is why Python dominates security scripting "
          "-- not raw execution speed."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK: TOOLS (industry-standard tools, what they do and why)
# ---------------------------------------------------------------------------
TOOLS_CHAPTERS = [
    C("tools_nmap", "Nmap: Network Scanning", [
        L("tools_01_01", "What Nmap Is For",
          "Nmap ('Network Mapper') is the standard tool for discovering "
          "hosts and services on a network -- which IPs are alive, which "
          "ports are open, and often what service/version is running on "
          "each. It's foundational to both offense and defense.",
          "What is Nmap primarily used for?",
          ["Editing web pages", "Discovering hosts, open ports, and services on a network", "Encrypting files", "Managing user passwords"], 1,
          "Nmap's core job is network and port discovery -- mapping what's "
          "actually reachable and listening."),
        L("tools_01_02", "Why Defenders Use Nmap Too",
          "It's not just an offensive tool -- Blue Teams regularly scan "
          "their own networks with Nmap to catch unexpected open ports or "
          "unauthorized devices before an attacker finds them first.",
          "Why would a defensive security team run Nmap against their own network?",
          ["They wouldn't, it's attack-only", "To discover unexpected open ports or unauthorized devices themselves, before attackers do", "To slow down their own network", "It's only used for compliance paperwork"], 1,
          "Self-scanning is standard defensive practice -- you want to find "
          "your own exposure before someone else does."),
        L("tools_01_03", "Scan Types, Conceptually",
          "Nmap supports many scan types -- a basic connect scan completes "
          "a full TCP handshake, while a SYN scan ('half-open') sends only "
          "the first packet, which is quieter and faster but requires "
          "elevated privileges to run.",
          "What's a practical tradeoff of a SYN ('half-open') scan versus a full connect scan?",
          ["SYN scans are always illegal", "SYN scans are typically quieter/faster but need elevated privileges", "There is no difference at all", "Connect scans don't use TCP"], 1,
          "SYN scans avoid completing the full handshake, making them "
          "faster and less likely to be logged by the target -- at the "
          "cost of needing raw socket privileges to run."),
        L("tools_01_04", "Authorization Still Applies",
          "Running Nmap against systems you don't own or have permission "
          "to scan is, in most places, illegal -- the tool being "
          "widely available and free doesn't change the legal requirement "
          "for authorization.",
          "Does Nmap being free and publicly available make scanning any target legal?",
          ["Yes, if a tool is public it's always legal to use on anyone", "No -- authorization to scan a specific target is still required regardless of tool availability", "Only if the scan is fast", "Only government agencies need authorization"], 1,
          "Tool availability has nothing to do with legality -- scanning "
          "requires the same authorization as any other testing activity."),
    ]),
    C("tools_wireshark", "Wireshark: Packet Analysis", [
        L("tools_02_01", "What Wireshark Shows You",
          "Wireshark captures and displays network traffic packet by "
          "packet, letting you inspect exactly what's being sent -- "
          "headers, protocols, and (for unencrypted traffic) the actual "
          "content, which is why it's a core learning tool for "
          "understanding protocols hands-on.",
          "What does Wireshark primarily let you do?",
          ["Edit files on a remote server", "Capture and inspect network traffic packet by packet", "Crack passwords offline", "Send phishing emails"], 1,
          "Wireshark is a packet capture and analysis tool -- it shows you "
          "exactly what traffic looks like at the protocol level."),
        L("tools_02_02", "Why Encryption Matters Here",
          "Wireshark can only show the *contents* of unencrypted traffic in "
          "plain text -- for HTTPS or other encrypted protocols, it can see "
          "that a connection exists, but not the actual encrypted payload "
          "without the right keys, which is exactly the protection TLS is "
          "designed to provide.",
          "Why can't Wireshark simply read the content of HTTPS traffic?",
          ["Wireshark is broken for HTTPS", "TLS encryption specifically prevents third parties from reading the payload without the keys", "HTTPS doesn't use packets", "It's a licensing restriction, not a technical one"], 1,
          "This is TLS doing exactly its job -- confidentiality against "
          "anyone observing the traffic, including tools like Wireshark, "
          "without the decryption keys."),
        L("tools_02_03", "Filters Are Everything",
          "With potentially thousands of packets captured per second, "
          "display filters (like `http` or `ip.addr == 10.0.0.5`) are "
          "essential to narrow down exactly what you're looking for instead "
          "of scrolling through noise.",
          "Why are display filters considered essential when using Wireshark?",
          ["They aren't, all packets are equally easy to review manually", "A capture can contain thousands of packets, and filters isolate what's actually relevant", "Filters encrypt the traffic", "Filters are only cosmetic"], 1,
          "Raw captures are often huge -- filters are what make the tool "
          "actually usable for finding something specific."),
        L("tools_02_04", "Common Defensive Use",
          "Blue Teams use packet capture to investigate incidents after "
          "the fact -- confirming exactly what data left the network, "
          "when, and to where, which is often critical evidence during "
          "incident response.",
          "How is packet capture commonly used defensively during incident response?",
          ["It isn't used defensively at all", "To reconstruct exactly what data was sent, when, and where during an incident", "Only to speed up the network", "To automatically block all traffic"], 1,
          "Captured traffic becomes forensic evidence -- reconstructing "
          "exactly what happened is a core part of incident investigation."),
    ]),
    C("tools_burp", "Burp Suite: Web Proxy Testing", [
        L("tools_03_01", "What a Web Proxy Does",
          "Burp Suite sits between your browser and a web application, "
          "letting you see and modify every request and response as it "
          "happens -- essential for authorized web application testing, "
          "where you need to manipulate parameters to check how the app "
          "handles unexpected input.",
          "What is the core function of a tool like Burp Suite?",
          ["Scanning Wi-Fi networks", "Intercepting and letting you inspect/modify web traffic between browser and server", "Cracking password hashes", "Sending mass emails"], 1,
          "It's an intercepting proxy -- positioned between client and "
          "server so every request/response can be inspected or altered."),
        L("tools_03_02", "The Repeater Concept",
          "A 'repeater' style feature lets a tester capture one request, "
          "then resend it repeatedly with small tweaked changes -- testing "
          "how an application responds to different input without having "
          "to manually redo an entire browser action each time.",
          "Why is a 'repeater' feature useful during web testing?",
          ["It automatically fixes vulnerabilities", "It lets you resend and tweak a captured request quickly, without redoing the whole browser flow", "It only works on image files", "It deletes application logs"], 1,
          "It massively speeds up manual testing -- capture once, then "
          "iterate on that single request as many times as needed."),
        L("tools_03_03", "Automated Scanning Within Scope",
          "Web proxies often include automated scanners that crawl an "
          "application and probe for common vulnerability classes -- "
          "useful for broad coverage, but professional testers always "
          "manually validate and go beyond what automation alone finds.",
          "What is a limitation of relying only on an automated web scanner?",
          ["Automated scanners always find every vulnerability", "It can miss business-logic flaws that require human understanding of the app's purpose",
           "It works only on desktop applications", "It has no limitations at all"], 1,
          "Automated tools are good at pattern matching, but flaws in "
          "business logic -- like a checkout process that lets you set a "
          "negative price -- usually need a human to actually notice."),
        L("tools_03_04", "Scope Discipline With Proxies",
          "Because a proxy tool intercepts everything passing through your "
          "browser, testers must be careful to only actively test in-scope "
          "targets -- accidentally sending crafted, modified requests to an "
          "out-of-scope site is a real and easy mistake to make.",
          "What is an easy mistake to make when using an intercepting proxy carelessly?",
          ["The tool prevents all mistakes automatically", "Accidentally sending modified/testing traffic to an out-of-scope site", "Proxies can't intercept HTTPS at all", "There's no risk since it's just a browser"], 1,
          "Because everything routes through the proxy, careless browsing "
          "during a testing session can accidentally send crafted traffic "
          "somewhere out of scope -- discipline matters."),
    ]),
    C("tools_metasploit", "Metasploit: Exploitation Framework", [
        L("tools_04_01", "What Metasploit Is",
          "Metasploit is a framework that organizes exploit modules, "
          "payloads, and post-exploitation tools into one consistent "
          "interface -- widely used in authorized penetration testing to "
          "reliably validate known vulnerabilities rather than writing "
          "custom exploit code from scratch for every single test.",
          "What is Metasploit's role in an authorized penetration test?",
          ["It's used to file legal paperwork", "It provides a standardized framework of exploit modules and payloads for testing known vulnerabilities",
           "It only scans for open ports", "It's exclusively used for defense, never offense"], 1,
          "It's an offensive framework -- standardizing how known "
          "vulnerabilities are validated during authorized testing."),
        L("tools_04_02", "Why It's Taught Defensively Too",
          "Blue Teams study Metasploit specifically to understand what "
          "signatures and behaviors its modules generate, so their "
          "detection tools can be tuned to catch it -- 'know your enemy's "
          "toolkit' applies to tools, not just tactics.",
          "Why would a defensive analyst study an offensive tool like Metasploit?",
          ["They wouldn't, it's irrelevant to defense", "To understand its behavior/signatures well enough to tune detection tools to catch it", "It's required to use antivirus software", "Only for entertainment"], 1,
          "Detection engineers often test their own tools against known "
          "frameworks like Metasploit specifically to validate their alerts "
          "actually fire."),
        L("tools_04_03", "Payloads, Conceptually",
          "A 'payload' is the code that runs after a vulnerability is "
          "successfully exploited -- in authorized testing, this is "
          "typically something benign that just proves access was gained, "
          "not something destructive.",
          "In an authorized, professional test, what does an exploitation payload typically do?",
          ["Permanently destroys the target system", "Proves access was gained, usually in a controlled, minimally invasive way", "Nothing, payloads aren't used in testing", "Automatically emails the CEO"], 1,
          "Professional testing uses controlled, minimally invasive "
          "payloads to prove impact -- not destructive ones, since the "
          "goal is a useful report, not damage."),
        L("tools_04_04", "Framework Availability vs Legality",
          "Like Nmap, Metasploit being free and widely available doesn't "
          "change the legal requirement for authorization -- using it "
          "against a system you don't have written permission to test "
          "is a crime, regardless of how accessible the tool is.",
          "Does a tool's free availability change the legal requirement to have authorization before using it on a target?",
          ["Yes, free tools are exempt from authorization requirements", "No -- authorization is required regardless of how available or well-known the tool is", "Only paid tools require authorization", "Authorization is only needed for government targets"], 1,
          "This point applies to every offensive tool in this app: "
          "availability and legality are completely separate questions."),
    ]),
    C("tools_siem", "SIEM & Blue Team Tooling", [
        L("tools_05_01", "SIEM Platforms in Practice",
          "Tools like Splunk and the Elastic Stack (ELK) are common "
          "real-world SIEM platforms -- ingesting logs from across an "
          "organization and giving analysts a searchable, dashboard-driven "
          "view instead of raw text files scattered across hundreds of "
          "servers.",
          "What core problem do SIEM platforms like Splunk or ELK solve?",
          ["They replace the need for firewalls", "Turning scattered raw logs from many systems into a searchable, centralized view", "They physically secure server rooms", "They write code automatically"], 1,
          "Centralization and searchability at scale is the core value -- "
          "raw logs scattered across hundreds of systems aren't useful "
          "without a way to search and correlate them."),
        L("tools_05_02", "Writing Detection Rules",
          "Analysts write detection rules/queries -- for example, alerting "
          "if the same account fails login more than 10 times in a minute "
          "-- turning raw log data into actionable alerts instead of just "
          "stored history nobody looks at.",
          "What turns raw stored logs into something actually useful for real-time defense?",
          ["Deleting old logs regularly", "Detection rules/queries that generate alerts on suspicious patterns", "Increasing log storage size", "Nothing, raw logs are sufficient alone"], 1,
          "Logs sitting unused provide no active defense -- rules that "
          "actively scan for suspicious patterns are what turn data into "
          "real-time detection."),
        L("tools_05_03", "Dashboards & Visibility",
          "A well-built SIEM dashboard gives a SOC team at-a-glance "
          "visibility -- login trends, alert volume, geographic anomalies "
          "-- so analysts can spot something 'off' visually before ever "
          "digging into raw data.",
          "What is the practical value of a good SIEM dashboard for a SOC team?",
          ["It has no practical value beyond decoration", "It provides at-a-glance visibility to help spot anomalies quickly", "It automatically fixes vulnerabilities", "It replaces the need for any analysts"], 1,
          "Visual, aggregated views help human analysts notice something "
          "unusual quickly, before drilling into the raw underlying data."),
        L("tools_05_04", "Password & Hash Tools, Conceptually",
          "Tools like John the Ripper or Hashcat test how resistant "
          "password hashes are to cracking -- used defensively to audit "
          "whether an organization's own stored password policies are "
          "actually strong enough, with explicit authorization to test "
          "those specific credentials.",
          "How are password-cracking tools like Hashcat used defensively?",
          ["They aren't, they're offense-only tools", "To audit whether an organization's own password policies actually hold up, with proper authorization", "To crack random strangers' accounts for fun", "Only to generate new passwords"], 1,
          "With explicit authorization, security teams audit their own "
          "password hashes to find weak, easily-cracked passwords before "
          "an attacker does."),
    ]),
]

# ---------------------------------------------------------------------------
# TRACK REGISTRY -- what the app actually loads
# ---------------------------------------------------------------------------
TRACKS: Dict[str, Dict[str, Any]] = {
    "networking": {
        "name": "Networking",
        "tagline": "The foundation everything else builds on.",
        "chapters": NETWORKING_CHAPTERS,
    },
    "blue_team": {
        "name": "Blue Team",
        "tagline": "Defense: monitoring, detection, response, hardening.",
        "chapters": BLUE_TEAM_CHAPTERS,
    },
    "red_team": {
        "name": "Red Team",
        "tagline": "Authorized offense: recon, vulns, exploitation, reporting.",
        "chapters": RED_TEAM_CHAPTERS,
    },
    "white_hat": {
        "name": "White Hat",
        "tagline": "Ethics, law, disclosure, bounties, and career paths.",
        "chapters": WHITE_HAT_CHAPTERS,
    },
    "black_hat": {
        "name": "Black Hat Awareness",
        "tagline": "Understand real threats to defend against them.",
        "chapters": BLACK_HAT_CHAPTERS,
    },
    "python": {
        "name": "Python Programming",
        "tagline": "The scripting skill every other track benefits from.",
        "chapters": PYTHON_CHAPTERS,
    },
    "tools": {
        "name": "Tools of the Trade",
        "tagline": "Nmap, Wireshark, Burp, Metasploit, SIEM, and more.",
        "chapters": TOOLS_CHAPTERS,
    },
}


def all_lesson_ids_for_track(track_id: str) -> List[str]:
    track = TRACKS[track_id]
    ids = []
    for chapter in track["chapters"]:
        for lesson in chapter["lessons"]:
            ids.append(lesson["id"])
    return ids


def total_lesson_count() -> int:
    return sum(len(all_lesson_ids_for_track(tid)) for tid in TRACKS)


def find_lesson(lesson_id: str):
    for track_id, track in TRACKS.items():
        for chapter in track["chapters"]:
            for lesson in chapter["lessons"]:
                if lesson["id"] == lesson_id:
                    return track_id, chapter["id"], lesson
    return None, None, None


