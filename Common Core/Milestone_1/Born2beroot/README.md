*This project has been created as part of the 42 curriculum by rmedonca.*

# Born2beRoot – README

## Table of Contents

1. [Description](#description)  
2. [Instructions](#instructions)  
3. [Installation](#installation)  
4. [sudo](#sudo)  
   - [Step 1: Installing sudo](#step-1-installing-sudo)  
   - [Step 2: Adding User to sudo Group](#step-2-adding-user-to-sudo-group)  
   - [Step 3: Running root-Privileged Commands](#step-3-running-root-privileged-commands)  
   - [Step 4: Configuring sudo](#step-4-configuring-sudo)  
5. [SSH](#ssh)  
   - [Step 1: Installing & Configuring SSH](#step-1-installing--configuring-ssh)  
   - [Step 2: Installing & Configuring UFW](#step-2-installing--configuring-ufw)  
   - [Step 3: Connecting to Server via SSH](#step-3-connecting-to-server-via-ssh)  
6. [User Management](#user-management)  
   - [Step 1: Setting Up a Strong Password Policy](#step-1-setting-up-a-strong-password-policy)  
   - [Step 2: Creating a New User](#step-2-creating-a-new-user)  
   - [Step 3: Creating a New Group](#step-3-creating-a-new-group)  
7. [cron](#cron)  
   - [Setting Up a cron Job](#setting-up-a-cron-job)  
8. [Resources](#resources)  
9. [Comparisons](#comparisons)  
10. [System Architecture Diagram](#system-architecture-diagram)
11. [AI Usage](#ai-usage)

---

## Description

The **Born2beRoot** project aims to configure a secure, minimal, and functional Linux environment in a virtual machine.

**Objectives:**

- Install and configure sudo, SSH, firewall, users, and groups.

- Apply strong password policies and privilege management.

- Automate tasks using cron.

**Operating System Choice:**

- Debian: stable, widely documented, active community support.

- Rocky Linux: enterprise-grade features, SELinux enabled by default.

**Main Design Choices:**

- Partitioning: Encrypted LVM volumes.

- Security: AppArmor for simplified access control.

- User Management: Strong password policies, sudo privileges, group management.

- Services Installed: SSH, UFW firewall, cron jobs.

---
## Instructions

1. Clone the repository:

```bash
$ git clone <repository-url>
$ cd born2beroot
```

2. Launch your virtual machine using VirtualBox or UTM.

3. Follow the steps in this README to configure:

- Sudo privileges

- SSH server and firewall

- User accounts and groups

- Password policies

- Cron jobs

4. Verify that all services are running correctly:

```bash
$ sudo systemctl status ssh
$ sudo ufw status
$ getent passwd
$ sudo crontab -u root -l
```

---

## Installation

- Set up the VM in **VirtualBox** (or UTM) without a graphical interface.  
- Create the hostname with your login followed by `42` (e.g., `rmedonca42`).  
- Configure encrypted partitions using **LVM** according to subject requirements.  

--- 

## sudo

### Step 1: Installing sudo
```bash
$ su -
# apt install sudo
# dpkg -l | grep sudo
```

### Step 2: Adding User to sudo Group

```bash
# adduser <username> sudo
# OR
# usermod -aG sudo <username>
$ getent group sudo
# reboot
$ sudo -v
```

### Step 3: Running root-Privileged Commands

Run all root commands using sudo, for example:

```bash
$ sudo apt update
```

### Step 4: Configuring sudo

Edit or create /etc/sudoers.d/<filename> and add:

```bash
Defaults        passwd_tries=3
Defaults        badpass_message="<custom-error-message>"
Defaults        logfile="/var/log/sudo/<filename>"
Defaults        log_input,log_output
Defaults        iolog_dir="/var/log/sudo"
Defaults        requiretty
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

Create the log directory:

```bash
$ sudo mkdir /var/log/sudo
```

## SSH

### Step 1: Installing & Configuring SSH

```bash
$ sudo apt install openssh-server
$ dpkg -l | grep ssh
$ sudo vi /etc/ssh/sshd_config
```

Configuration:

```text
Port 4242
PermitRootLogin no
```

Restart and check:

```bash
$ sudo service ssh status
$ systemctl status ssh
```

### Step 2: Installing & Configuring UFW

```bash
$ sudo apt install ufw
$ dpkg -l | grep ufw
$ sudo ufw allow 4242
$ sudo ufw enable
$ sudo ufw status
```

### Step 3: Connecting to Server via SSH

```bash
$ ssh <username>@<ip-address> -p 4242
$ logout
$ exit
```


## User Management
### Step 1: Setting Up a Strong Password Policy

Edit /etc/login.defs:

```bash
PASS_MAX_DAYS   30
PASS_MIN_DAYS   2
PASS_WARN_AGE   7
```

Install PAM password quality module:

```bash
$ sudo apt install libpam-pwquality
$ dpkg -l | grep libpam-pwquality
$ sudo vi /etc/pam.d/common-password
```

Final line example:

```bash
password requisite pam_pwquality.so retry=3 minlen=10 ucredit=-1 dcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root
```

### Step 2: Creating a New User

```bash
$ sudo adduser <username>
$ getent passwd <username>
$ sudo chage -l <username>
```

### Step 3: Creating a New Group

```bash
$ sudo addgroup user42
$ sudo adduser <username> user42
$ sudo usermod -aG user42 <username>
$ getent group user42
```

## cron

Edit cron as root:

```bash
$ sudo crontab -u root -e
```

To run a script every 10 minutes:

```bash
*/10 * * * * sh /path/to/script
```

Check scheduled jobs:

```bash
$ sudo crontab -u root -l
```

## Resources

- [Debian Documentation](https://www.debian.org/doc/)
- [Cron Manual](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [UFW Documentation](https://help.ubuntu.com/community/UFW)
- [PAM Password Quality](https://linux.die.net/man/8/pam_pwquality)
- Tutorials on VirtualBox, UTM, LVM, and SSH configuration

## Comparisons

| Feature          | Choice in Project | Alternative | Notes                                                                                           |
| ---------------- | ----------------- | ----------- | ----------------------------------------------------------------------------------------------- |
| Operating System | Debian            | Rocky Linux | Debian is stable with extensive documentation; Rocky offers enterprise-level SELinux by default |
| Security Module  | AppArmor          | SELinux     | AppArmor is simpler to configure; SELinux is more granular but complex                          |
| Firewall         | UFW               | firewalld   | UFW is user-friendly; firewalld provides more advanced rules for enterprises                    |
| Virtualization   | VirtualBox        | UTM         | VirtualBox is widely used and well-documented; UTM is optimized for macOS M1/M2                 |

## System Architecture Diagram

```text
          +---------------------+
          |      Host OS        |
          | (Windows/macOS/Linux)|
          +---------------------+
                    |
                    v
          +---------------------+
          | Virtual Machine     |
          | (VirtualBox / UTM)  |
          +---------------------+
                    |
                    v
     +--------------------------------+
     |          Debian VM             |
     +--------------------------------+
     | Partitioning: Encrypted LVM   |
     | Security: AppArmor            |
     | Firewall: UFW                 |
     | SSH: Port 4242                |
     | Users & Groups Management     |
     | Cron Jobs                     |
     +--------------------------------+
```

## AI Usage

AI was used to improve the structure, readability, and clarity of this README.
No code or VM configuration was generated or executed with AI — only documentation editing.