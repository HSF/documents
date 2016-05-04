---
title: Proposal for HSF Project Best Practices
TN-ID: TN-draft
author: "Benedikt Hegner"
institutes: CERN
date: date empty
abstract: This technical note is a proposed list of best practices for HSF projects. The main motivation is to ensure interoperability and usability of a given project in other projects and being able to build consistent software stacks. In addition it should make it easier for other developers to contribute to existing projects.
---

# Introduction

This technical note is a proposed list of best practices for HSF projects. The main motivation is to ensure interoperability and usability of a given project in other projects and being able to build consistent software stacks. In addition it should make it easier for other developers to contribute to existing projects. In the following we discuss different practices and conventions that ease the life of
  * developers and new contributors
  * end-users and other client projects 
 
Afterwards we provide a little checklist of the proposals you may want to use for your project. The proposals are mainly based on experience with the LCG software projects and releases. You may find most of the points discussed here trivial. However people usually differ in what they consider trivial. The technical recommendations in this document are tailored towards C++-based projects, but can easily be mapped onto e.g. Python-based projects.

# Project Scope, Name and Visibility

On starting a project, make sure you have an idea of the project's scope and goals. Try to pick a name that is suitable for that. You need to ensure uniqueness, as the name will be used to name software artifacts like libraries, code namespaces, error messages, etc.. In addition, have a look around whether it conflicts with pre-existing trademarks for software products or services.

Though it sounds like a triviality, your project should be made known to the community. For this, having a *dedicated project website* or another entry point for information is essential. It should concentrate all the information useful for users and developers. If possible, it should point at all the other information listed in this document. It is important to find the right place to put information. Try not to repeat yourself, as duplicated documentation can easily run out of sync. Access to all sources of project information should be granted to search engine spiders. Furthermore, the HSF provides a knowledge-base, where your project could be announced.


# Supporting Developers and Contributors
The following sections discuss points mainly relevant for project developers and potential new contributors.

## Code repository
The first requirement for an open-source project is fully versioned code in a *public repository*. The code should be accessible in anonymous read-only mode by anybody. Services like GitHub or GitLab provide it for free. In addition efforts like [hepforge](https://www.hepforge.org/) or labs like CERN or DESY may host HEP-specific packages. Services supporting a clone plus *merge-request/pull-request workflow* can be helpful to attract new contributors.

## License
The code and software provided should be properly licensed in order to be able to use code provided by others, and to allow people to re-use, update, or improve the software you provide. The [HSF technical note](http://hepsoftwarefoundation.org/technical_notes.html) *HSF-TN-2016-01* (*Software Licence Agreements HSF Policy Guidelines*) discusses various options. This is one of the topics that is typically ignored at the beginning of a project and hard to fix afterwards.

## Compilation and other commands
Compiling, installing and testing should be - if possible - each single-command actions for building, installing and testing. In particular making testing easy is useful. A good place to put the necessary information is a *README* file in the repository. Relying on community standards like *CMake* make it easier for others to use and understand the setup.

## Testing
To improve on the quality of software, unit and integration testing are essential. Having well-documented tests makes it as well easier for contributors to participate. They can check whether they break old features and can with new tests document what their addition is supposed to do. 

For *unit tests* plenty of software packages exist, of which *gtest* and *catch* are two good choices. Integration tests running a software project in a certain setup can take advantage of *CTest* and *CDash* or be driven by shell scripts. Ease of use is again important here, otherwise tests tend not to be run.

## Communication and Reporting
A mailing list to contact developers is always useful. Better to have publicly and anonymously accessible archives and be open for subscription and posting by the public.

## Issue tracking 
It is useful to provide an issue (bug) tracker for users and developers to interact with, allowing to view of both open and closed tickets anonymously by the public. Possible solutions here are the issue tracking capabilities of GitHub projects or CERN's JIRA service.

## Reference Guide
For developers it is important to have a good overview of provided interfaces, existing classes, and implementation details. For this a reference guide is a helpful tool. A de-facto standard for creating reference guides in C++ projects is *Doxygen*. 

## Conventions and Workflows
Every project choses certain (coding) conventions and workflows. While there is a plethora of possibilities, the concretely chosen conventions and workflows should be documented visibly. A *How to contribute* document is a good practice. This is as well a nice place to add information where contributions by others would be possible and desired.


# End-users and client projects

## Documentation
In addition to the already mentioned documentation, an end-user focused documentation is important. A little checklist further below summarizes the most important information to be given as part of the documentation.
 
## Release Information
While developers (most of the time) know the changes between various releases, it is important to document changes between releases for end-users. It turned out to be a good policy to have multiple categories of releases, like production releases, development releases, bug fix releases, etc. While each project may have different conventions there, the chosen convention should be explained. A clear numbering scheme like "major.minor.patch" can support this. For each release the *supported compilers*, *supported operating systems* and *required dependencies* should be listed. This helps avoiding frustrations on user side.

## Interaction with developers
To be able to interact with developers, both the already mentioned *mailing list* and *issue tracker* are important and helpful. The required permissions to post there should be as low as possible. Make it easy for people to give feedback.

## Relocatability and co-existence of versions
Often a project has to be integrated into bigger software stacks. Being relocatable, i.e. having no hard-coded paths in any build artifact, is often a necessity to deploy and distribute these stacks. To enable your project to become part of such a software stack, try to make it relocatable. In addition your software should not make too strong assumptions about its own location.

## Usability and run-time settings
It should be straight forward for a user to set up and run your project. This can for example be ensured by providing environment setup scripts.

# Making best practices easier - the HSF Template Project
Many of the points mentioned are per se trivial, but need some infrastructure to be set up. To assist new projects, an HSF project template was created. It covers many of the technical points and provides some canonical or example implementation for many of the issues. It is meant as open collection point of ideas and proposals by the community. More details are to be found in an upcoming HSF technical note.


# Checklist
A little checklist of topics to consider is given here. Not every point applies to every project, but it may give you a handle in improving the quality of the software you provide.


## Repository and code checklist

| Topic              | Done  | Possible solution(s)   | Template  |
| ------------------ |-------|:----------------------:| ---------:|
| Public repository  |       | github, gitlab         | -         |
| License + file     |       | MIT, GPL               | MIT, GPL  |
| README file        |       |  -                     | Yes       | 
| Reference guide    |       | Doxygen                | Doxygen   |
| build scripts      |       | CMake                  | CMake     |
| Unit testing       |       | gtest, catch           | catch     |
| Integration testing|       | CTest, scripts         | CTest     |
| version file       |       | headers                | headers   |
| Relocatability     |       | strict policy          | Yes       |
| environment setup  |       | (c)sh script           |  -        |


## Procedure and release checklist 
The following list contains mostly "nice-to-have" points. 

| Topic             | Done  | Possible solution(s)   | Template  |
| ----------------- |-------|:----------------------:| ---------:|
| Defined workflow  |       | plenty                 |           |
| Automatic testing |       | travis CI, gitlab CI   | -         |
| Test run+reporting|       | CTest,CDash            | CTest     |
| Static Analysis   |       | clang-analyzer, SAS    | -         |


## Website and information checklist

| Topic                           | Done  | Possible solution(s)   |
| ------------------------------- |-------|:----------------------:|
| Website                         |       | jekyll, github pages   |
| How to contribute               |       | -                      |
| User manual                     |       | markdown, doxygen      |
| Reference manual                |       | doxygen                |
| Bug tracker                     |       | github, gitlab, jira   |  
| Mailing list                    |       | google groups, e-groups| 
| Link to repository              |       | -                      |
| List of releases                |       | -                      |
| List of supported OS+compilers  |       | -                      |
| List of pre-requisites          |       | -                      |
| Registered in HSF knowledge base|       | -                      |


# Summary and Outlook

This document described a few best practices, and potential implementations.  This is work in progress and every input, addition or correction by the community is welcome!
