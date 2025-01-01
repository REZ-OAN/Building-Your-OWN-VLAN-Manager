# VLAN-Management-Tool

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [My Findings](#my-findings)
- [Steps To Follow](#steps-to-follow)
- [References](#references)

## Introduction 
A VLAN Management System or Tool is a software application or platform designed to help network administrators configure, monitor, and manage Virtual LANs (VLANs). VLANs are logical subnets or segments of a physical network, created to improve network organization, security, and performance by isolating different groups of devices.

### Purpose of a VLAN Management Tool
The primary goal of such a tool is to simplify and streamline the process of managing VLANs by providing an easy-to-use interface for tasks like creating VLANs, assigning devices to VLANs, and troubleshooting connectivity issues.

To build a lightweight, user-friendly tool to create, configure, and manage VLANs. I am planning the tool should simulate VLANs in a Docker-in-Docker (DinD) environment to avoid physical hardware requirements.
### Scope
- VLAN creation and tagging.
- Network segmentation and interface assignment.
- Basic network troubleshooting (e.g., ping, traceroute).
- Visualization of VLAN topology and configuration.

## Requirements
- Knowledge of Linux and Bash Scripting
- Intermediate knowledge of Docker 
## My Findings
- Creating Dind Image From Scratch
## Steps To Follow
- [Setting up `DIND` image](./docs/dind_image_creation.md)

## References
- [Creating a Docker in Docker (DinD) container with any base image](https://medium.com/@ferdinandklr/creating-a-docker-in-docker-dind-container-with-any-base-image-7ce3a4d44021)