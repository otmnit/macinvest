# 🔎 MAC Investigator

> A lightweight network investigation tool for tracing MAC addresses across network infrastructure.

**MAC Investigator** helps network engineers quickly investigate where a device is connected in the network.

Given a MAC address, the goal is to identify:

**MAC Address → Network Device → Interface / Port**

---

## 🚀 Why?

Finding the physical location of a device on a network can be surprisingly time-consuming.

Normally, an engineer has to:

1. Search for the MAC address
2. Identify the switch
3. Check the corresponding interface
4. Follow uplinks if necessary
5. Continue until reaching the access switch

MAC Investigator aims to simplify this workflow.

---

## ✨ Features

Current project direction:

* 🔍 MAC address lookup
* 🌐 Network device identification
* 🔌 Switch interface identification
* 🧭 MAC tracing across network infrastructure
* 💻 CLI-oriented workflow
* 🧱 Designed to support multiple network vendors (Cisco, Juniper, Arista)

### Planned

* CDP / LLDP topology discovery
* Automatic uplink traversal
* Multi-device investigation
* Export results as JSON
* Web interface
* API
* NetBox integration
* LibreNMS integration

---

## 🧠 Concept

The core workflow is:

```text
             MAC Address
                  │
                  ▼
        ┌──────────────────┐
        │ MAC Investigator │
        └────────┬─────────┘
                 │
                 ▼
          Network Switch
                 │
                 ▼
            MAC Table
                 │
                 ▼
          Interface / Port
                 │
                 ▼
         Connected Device
```

For future, the tool will progressively follow the topology:

```text
MAC
 │
 ▼
Core Switch
 │
 └── Uplink
       │
       ▼
 Distribution Switch
       │
       └── Uplink
             │
             ▼
          Access Switch
             │
             ▼
          Gi1/0/24
```

---

## 🛠️ Tech Stack

The project is intentionally lightweight.

* Python
* SSH / network CLI
* Netmiko
* TextFSM / structured parsing
* JSON
* Git

Future integrations may include:

* NetBox
* LibreNMS
* REST APIs
* Docker

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/otmnit/macinvest.git
cd macinvest
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Example:

```bash
python main.py --mac aa:bb:cc:dd:ee:ff
```

Example output:

```text
MAC Investigator
────────────────────────────

MAC Address : aa:bb:cc:dd:ee:ff

Device      : SW-CORE-01
Vendor      : Cisco

Interface   : Gi1/0/24
Status      : Connected

Next Hop    : None

Result:
→ Device found on SW-CORE-01 Gi1/0/24
```

---

## 🧪 Project Status

**Early development / MVP**

The current version focuses on establishing the core investigation workflow before adding automation and topology discovery.

---

## 🗺️ Roadmap

### V0.1 — Foundation

* [x] Project structure
* [ ] CLI
* [ ] MAC validation
* [ ] MAC normalization
* [ ] Basic lookup

### V0.2 — Network Investigation

* [ ] Cisco MAC table parsing
* [ ] Interface identification
* [ ] SSH connection
* [ ] Basic error handling

### V0.3 — Topology

* [ ] CDP discovery
* [ ] LLDP discovery
* [ ] Uplink detection
* [ ] Automatic MAC traversal

### V0.4 — Multi-Vendor

* [ ] Cisco
* [ ] Juniper
* [ ] Huawei
* [ ] Arista

### V1.0 — Network Tool

* [ ] API
* [ ] Web UI
* [ ] NetBox integration
* [ ] LibreNMS integration
* [ ] Docker deployment

---

## 🎯 Long-Term Vision

MAC Investigator is intended to evolve from a simple CLI utility into a small network investigation platform.

The long-term workflow:

```text
                  ┌─────────────┐
                  │ MAC Address │
                  └──────┬──────┘
                         │
                         ▼
                ┌─────────────────┐
                │ MAC Investigator│
                └────────┬────────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           NetBox     LibreNMS    Network CLI
             │           │           │
             └───────────┼───────────┘
                         ▼
                  Network Topology
                         │
                         ▼
                   Final Switch
                         │
                         ▼
                    Access Port
```

---

## 🤝 Contributing

Contributions, ideas and improvements are welcome.

Feel free to open an issue or submit a pull request.

---

## 📄 License

MIT License.
