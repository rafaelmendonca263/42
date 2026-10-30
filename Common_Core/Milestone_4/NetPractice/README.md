*This project has been created as part of the 42 curriculum by rmedonca.*

![School](https://img.shields.io/badge/School-42-black)
![Topic](https://img.shields.io/badge/Topic-Networking-blue)
![Protocol](https://img.shields.io/badge/Protocol-TCP%2FIP-orange)
![Layer](https://img.shields.io/badge/Layer-OSI%20L2%2FL3-purple)
![Status](https://img.shields.io/badge/Status-Completed-success)

# NetPractice

## Description

NetPractice is a practical project designed to introduce the fundamentals of computer networking. The goal of this project is to configure small-scale simulated network topologies to establish proper communication between host devices and routers.

Through 10 progressive levels, this project covers essential networking concepts such as IP addressing, subnet masking, network segmentation, default gateways, and static routing tables.

---

## Instructions

### Prerequisites

* A modern web browser.
* Bash shell (Unix-like environment).
* Python 3 (optional, used as an alternative local web server).

### How to Run the Training Interface

1. Download or clone this repository containing the NetPractice interface.
2. Execute the setup script from the root directory:
   ```bash
   ./run.sh
   ```
   This will launch a local web server and automatically open the interface in your default browser.

3. **Alternative Launch Method:**
   If `run.sh` does not work, run Python's built-in HTTP server:
   ```bash
   python3 -m http.server 49242
   ```
   Then open your browser and navigate to `http://localhost:49242`.

### Solving Levels and Exporting Configurations

1. Enter your **42 login** in the intranet login field on the welcome screen to load your personal configuration (or select the **Evaluation** tab to generate evaluation setups).
2. For each level (from Level 1 to Level 10):
   * Modify the unshaded network configuration fields (IP addresses, subnet masks, gateways, routing tables).
   * Click **[Check again]** to verify your configuration. Use the logs at the bottom to debug routing errors or invalid IPs.
   * Once solved, click **[Get my config]** to download your configuration file.
3. Save each exported file directly into the **root** of your repository.

---

## Submission Requirements

The repository root must contain exactly 10 configuration files exported from the interface (one for each level) along with this `README.md`:

```text
.
├── level1
├── level2
├── level3
├── level4
├── level5
├── level6
├── level7
├── level8
├── level9
├── level10
└── README.md
```

> **Evaluation Note:** During peer-evaluation, you will be required to solve 3 randomly generated levels within a limited timeframe. No external network calculation tools are permitted, though basic CLI tools like `bc` or manual calculations are allowed.

---

## Resources

### Core Networking Concepts Studied

To successfully complete the 10 levels of NetPractice, key theoretical and practical concepts of network architecture and TCP/IP protocol principles were applied.

#### 1. IPv4 Structure & Subnet Masking

An IPv4 address is a 32-bit identifier in dotted-decimal format (`Octet1.Octet2.Octet3.Octet4`), split into two logic parts: **Network ID** and **Host ID**.

* **Subnet Mask:** Defines the prefix length via contiguous `1` bits (Network) followed by `0` bits (Host).
* **Network Calculation:** Extracted by bitwise `AND` operation (`IP AND Mask`).

| Concept | Binary / Bit Representation | Function | Usable as Host IP? |
| :--- | :--- | :--- | :---: |
| **Network Address** | Host bits all set to `0` | Identifies the subnet range | ❌ No |
| **Usable Host Range** | Host bits between min and max | Assigned to interfaces / hosts | ✅ Yes |
| **Broadcast Address** | Host bits all set to `1` | Targets all hosts in the subnet | ❌ No |

> 📐 **Usable Hosts Formula:** $2^{(32 - \text{CIDR})} - 2$  
> *Example:* `/28` mask (`255.255.255.240`) $\rightarrow 2^{(32-28)} - 2 = 16 - 2 = \mathbf{14\text{ usable IPs}}$.

---

#### 2. Device Roles: Switches vs. Routers

| Feature | Switch | Router |
| :--- | :--- | :--- |
| **OSI Layer** | Layer 2 (Data Link) | Layer 3 (Network) |
| **Addressing** | MAC Addresses | IP Addresses |
| **Function** | Connects devices inside the **same** subnet | Connects and forwards traffic **between** subnets |
| **Interfaces** | Single broadcast domain across ports | Each interface belongs to a **different** subnet |

---

#### 3. Gateway Decision & Traffic Routing Flow

When a host wants to transmit an IP packet, it compares the destination IP with its own local subnet range:

```text
               +----------------------------------+
               | Is Destination in Local Subnet? |
               +----------------------------------+
                                |
               +----------------+----------------+
               |                                 |
           [ YES ]                            [ NO ]
               |                                 |
               v                                 v
   Send directly to host           Send packet to Default Gateway
   via local Layer 2 connection     (Router IP in local subnet)
```

* **Default Gateway Rule:** Must reside on the **same subnet** as the source host interface.
* **Two-Way Reachability:** Traffic routing requires both a valid **Forward Path** ($Host A \rightarrow Host B$) and **Return Path** ($Host B \rightarrow Host A$).

---

#### 4. Static Routing Tables

Routing tables determine packet forwarding decisions based on destination entries:

* **Default Route (`0.0.0.0/0`):** Catch-all route used when no specific route exists for a destination.
* **Longest Prefix Match:** If multiple routes match a destination address, the router selects the entry with the most specific mask (highest CIDR prefix).

---

#### 5. OSI Model Layer Mapping

| Layer | Name | Function in NetPractice |
| :---: | :--- | :--- |
| **L1** | Physical | Cable connections and interface link states |
| **L2** | Data Link | Direct communication within the same network segment |
| **L3** | Network | IP Addressing, Subnet Masks, Gateways, and Static Routing |

---

### Artificial Intelligence Usage

AI tools (such as ChatGPT / Claude) were used responsibly in compliance with 42 AI guidelines:

* **Scope of Tasks:** Clarifying mathematical concepts (e.g., bitwise `AND` for subnet ranges), verifying host calculations for non-standard masks (`/27`, `/29`), and interpreting simulator debug logs.
* **Verification:** All AI explanations were double-checked against technical docs, validated by solving simulator levels manually, and discussed with peers. No automated scripts or AI tools were used to auto-solve the levels.