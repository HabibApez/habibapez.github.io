---
title: "Quadcopter Digital Control System"
excerpt: "Design and implementation of digital control for a quadcopter axis, archived in the Instituto Politecnico Nacional thesis repository."
tech_stack:
  - C
  - dsPIC
  - LabVIEW
  - Control Systems
thumbnail: /assets/images/projects-quadcopter.png
github_repo:
order: 1
phase: completed
status: "Archived Thesis"
last_updated: "September 2026"
---

## Problem Statement

Stabilizing UAV dynamics on constrained embedded hardware requires robust control design and practical implementation constraints. This project implements digital control for a quadcopter axis from a seesaw-based systems perspective.

## Methodology and Approach

1. Build and validate dynamic model of single-axis behavior.
2. Design discrete controller and tune stability margins.
3. Implement on dsPIC platform and integrate instrumentation.
4. Compare simulation and physical test response curves.

## System Overview

The experimental platform reduces quadcopter attitude control to one rotational axis. Two opposing motor-propeller assemblies are mounted at the ends of a balanced arm, allowing controller behavior to be studied without the uncontrolled motion of a free-flying vehicle.

The closed-loop system consists of:

- A seesaw-style mechanical plant representing one quadcopter axis.
- Two motor-propeller actuators that generate opposing torque.
- An inertial sensor that measures the arm's angular response.
- A dsPIC microcontroller that samples feedback and executes the digital controller.
- Power electronics that translate the controller output into motor commands.
- A LabVIEW interface used for monitoring, data acquisition, and experimental analysis.

At each control step, the measured angle is compared with the requested reference. The resulting error is processed by the digital controller, which adjusts the motor commands to stabilize the arm and track the target angle. This constrained setup makes it possible to compare simulated and physical responses under repeatable conditions.

![Physical quadcopter single-axis control test bench]({{ '/assets/images/projects-quadcopter.png' | relative_url }})

*Physical single-axis test bench used to evaluate the quadcopter control strategy.*

## Outcomes

- Demonstrated stable transient response through simulation and physical testing alignment.
- Produced publication-backed evidence of robust controller implementation on embedded hardware.
- Established the control-theory foundation that now informs my safety-critical AI research direction.

## Thesis and Supporting Material

The thesis is available through the official IPN repository and as a local PDF copy. The original implementation source code has not yet been recovered.

- [Official IPN record](https://tesis.ipn.mx/handle/123456789/17521)
- [Read the thesis (PDF)]({{ '/assets/docs/quadcopter-digital-control-thesis.pdf' | relative_url }})
