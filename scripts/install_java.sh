#! /bin/bash

# Install Java 17
sudo apt update
sudo apt install -y openjdk-17-jdk

# Set java 17 as default
echo "Setting Java 17 as the default system version..."
sudo update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java
sudo update-alternatives --set javac /usr/lib/jvm/java-17-openjdk-amd64/bin/javac

JAVA_VERSION=$(java --version 2>&1 | head -n 1)

# Verify installation
echo "======================================"
echo "   Java instllation complete   "
echo "   Your Java version: $JAVA_VERSION"
echo "======================================"
