# Text-Fixture-Generation

## Introduction

Fixture-TCG is the first fixture-aware automated test generation framework described in the paper "Bridging the Fixture Gap in Test Generation: The Fixture-TCG Approach and Benchmark"

Fixture-TCG addresses the critical "Fixture Gap" in unit testing by treating fixture construction as a proactive diagnostic process. It introduces FixtureEval, the first benchmark explicitly designed to measure fixture reasoning capabilities. FixtureEval consists of 600 functions drawn from 20 popular GitHub repositories, complemented by a manually implemented leakage-free subset to prevent data contamination. Each function is precisely annotated with its fixture dependency, enabling a dual evaluation on both classification and generation capability.

Fixture-TCG is open for research purposes, enabling thorough evaluation of LLMs' capabilities in autonomously constructing multi-step fixture environments and executable unit tests.

## Dataset

The experimental evaluation is conducted on FixtureEval, a benchmark specifically designed to address the lack of fixture-aware metrics in existing datasets. As shown in the directory structure, the benchmark comprises three distinct components:

- **FixtureEval-Github** (`dataset/github`): Contains real-world Python functions collected from popular repositories to evaluate performance in realistic scenarios.
- **FixtureEval-Leakage-Free** (`dataset/leakage-free`): Consists of functions meticulously constructed by experts. This subset serves as a rigorous safeguard against data leakage, ensuring that LLMs cannot rely on memorized training data.
- **FixtureEval-Java** (`dataset/java`): A Java extension of the benchmark used to evaluate Fixture-TCG's cross-language generalization capability.

## Open-Source Code

## Environmental Requirements

## Research Questions (RQs)

## Getting Started

## Requirements

