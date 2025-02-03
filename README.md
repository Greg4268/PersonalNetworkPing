# 📶 Hilbert Curve from Network Ping

This Python program dynamically detects the user's network and subnet mask, then scans all available IP addresses by sending ping requests to determine which devices are active. The results are visualized using a Hilbert curve, which plots active and inactive IPs in a structured 2D representation. 

## 📌 Features
- Dynamically detects user's network and subnet mask
- Scans network for active IP addresses using ping requests
- Creates visualization using Hilbert curve

## Sample from my home network 
![Alt text](./HilbertCurveImg.png)

## 🚀 Quick Start Guide

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/Greg4268/PersonalNetworkPing
cd PersonalPingNetwork
```
### 2️⃣ **Set up a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate
```
### 3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```
### 4️⃣ **Run The Program** 
```sh
python ping.py
```

## Notes: 
- This program could likely be sped up greatly by adjusting the ping logic

## Special Credit
This project was inspired by suckerpinch's YouTube video "Harder Drive: Hard drives we didn't want or need" Link: https://www.youtube.com/watch?v=JcJSW7Rprio



