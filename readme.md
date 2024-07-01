# ArtifactForge

ArtifactForge is a flexible and extensible library for creating and managing various types of artifacts, with a focus on media-related functionalities.

![Basic structure of the Artifact superclass](artifact_structure.png)

## Table of Contents
1. [Base Structure](#base-structure)
2. [Mixin Logic](#mixin-logic)
3. [Concrete Artifacts](#concrete-artifacts)
4. [Combined Artifacts](#combined-artifacts)
5. [JSON Formatting](#json-formatting)
6. [How This Structure Works](#how-this-structure-works)
7. [Maintaining the Structure](#maintaining-the-structure)
8. [Usage Examples](#usage-examples)

## Base Structure

The `Artifact` class serves as the base class for all artifacts in the library. It defines common attributes and methods that are shared among different types of artifacts. The base structure includes:

- `prompt`: A dictionary representing the prompt or input for the artifact.
- `payload_data`: Additional data that can be used in conjunction with the prompt.
- `mandatory_tags`: A dictionary of mandatory tags associated with the artifact.
- `optional_tags`: A dictionary of optional tags associated with the artifact.
- `data`: The generated data of the artifact.
- `metadata`: Additional metadata related to the artifact.
- `constructed`: A boolean indicating whether the artifact has been constructed.

## Mixin Logic

The library utilizes mixin classes to add specific functionalities to artifacts. The `MediaMixin` class is an example of a mixin that provides media-related properties and methods, such as `start_time`, `end_time`, and `duration`.

Mixins allow for code reuse and help keep the artifact classes focused on their core responsibilities.

## Concrete Artifacts

Concrete artifact classes inherit from the `Artifact` base class and implement specific functionality. The `WebScraperArtifact` class is an example of a concrete artifact that performs web scraping tasks.

Concrete artifacts override the `build` and `generate_data` methods to provide custom behavior based on their specific requirements.

## Combined Artifacts

Artifacts can be combined with mixins to create more specialized artifacts. For example, a `MediaWebScraperArtifact` can be created by inheriting from both the `WebScraperArtifact` and `MediaMixin` classes.

Combined artifacts inherit the attributes and methods from both the base artifact class and the mixin classes.

## JSON Formatting

The library uses JSON formatting for the `prompt`, `mandatory_tags`, `optional_tags`, `data`, and `metadata` attributes. JSON provides a standardized and portable format for data exchange and storage.

The `is_json_serializable` function is used to check if a given data is JSON serializable, ensuring that the data can be properly serialized and deserialized.

## How This Structure Works

The artifact structure in ArtifactForge follows a hierarchical approach:

1. The `Artifact` class defines the base structure and common attributes for all artifacts.
2. Mixin classes, such as `MediaMixin`, provide additional functionalities that can be added to artifacts.
3. Concrete artifact classes, such as `WebScraperArtifact`, inherit from the `Artifact` class and implement specific behavior.
4. Combined artifacts can be created by inheriting from both a concrete artifact class and one or more mixin classes.

This structure allows for code reuse, modularity, and extensibility. New artifact types can be easily added by creating new concrete classes, and existing artifacts can be enhanced with additional functionalities through mixins.

## Maintaining the Structure

To maintain the structure and integrity of the ArtifactForge library, follow these guidelines:

- When creating new artifact classes, inherit from the `Artifact` base class and implement the required methods.
- Use mixin classes to add specific functionalities to artifacts, keeping the mixin classes focused and reusable.
- Ensure that the `prompt`, `mandatory_tags`, `optional_tags`, `data`, and `metadata` attributes are JSON serializable.
- Use the `is_json_serializable` function to validate the serializability of data before assigning it to artifact attributes.
- Follow Python conventions and best practices, such as using type hints, modular code organization, and meaningful variable and function names.

## Usage Examples

Here are a few examples of how to use the ArtifactForge library:

```python
# Creating a WebScraperArtifact
url = 'https://example.com'
artifact = WebScraperArtifact.build(url)
artifact.construct()

# Accessing artifact attributes
print(artifact.prompt)
print(artifact.data)
print(artifact.metadata)
```