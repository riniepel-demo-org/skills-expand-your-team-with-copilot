# Mergington High School Activities

A comprehensive web application that allows teachers to manage student registrations for extracurricular activities at Mergington High School.

## Features

### For Teachers
- **Secure Authentication** - Login with teacher credentials to access management features
- **Student Registration Management** - Sign up students for activities and remove registrations
- **Session Management** - Persistent login sessions with automatic validation

### For Students & Visitors
- **Browse Activities** - View all available extracurricular activities with detailed information
- **Advanced Filtering** - Filter activities by:
  - Day of the week (Monday through Sunday)
  - Time of day (Before School, After School, Weekend)
- **Real-time Information** - See current participant counts and capacity limits
- **Responsive Design** - Optimized for desktop and mobile devices

### Activity Management
- **Diverse Program Offerings** - 12+ activities including:
  - Academic clubs (Chess Club, Math Club, Programming Class)
  - Sports teams (Soccer, Basketball)
  - Arts programs (Art Club, Drama Club)
  - Weekend programs (Robotics Workshop, Science Olympiad)
- **Flexible Scheduling** - Activities scheduled across all days of the week including weekends
- **Capacity Management** - Track and enforce participant limits per activity
- **Detailed Schedules** - Precise time slots from early morning to evening

## Technology Stack

- **Backend**: FastAPI with Python
- **Database**: MongoDB for data persistence
- **Frontend**: HTML, CSS, and vanilla JavaScript
- **Authentication**: Secure password hashing with Argon2
- **API**: RESTful endpoints with automatic documentation

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
