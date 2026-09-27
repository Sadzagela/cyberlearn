# Security Policy

## Supported Versions

Security fixes are generally applied to the latest version of CyberLearn available on the repository's default branch.

| Version               | Supported      |
| --------------------- | -------------- |
| Latest release        | ✅ Yes          |
| Development version   | ✅ Yes          |
| Older releases        | ⚠️ Best effort |
| Unmaintained versions | ❌ No           |

If you are unsure whether your version is supported, update to the latest version before reporting a vulnerability.

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in CyberLearn, report it privately to the project maintainers through the repository's GitHub security reporting mechanism, if enabled.

If private vulnerability reporting is not enabled, contact the repository owner through a private GitHub communication channel.

When reporting a vulnerability, please include as much of the following information as possible:

* A clear description of the vulnerability
* The affected version or commit
* Steps required to reproduce the issue
* The expected behavior
* The actual behavior
* Potential security impact
* Any relevant logs or error messages
* A minimal proof of concept, when appropriate

Please avoid including real credentials, personal information, or other sensitive data in a report.

---

## What to Report

Examples of security issues that should be reported privately include:

* Arbitrary code execution
* Unsafe file handling
* Path traversal
* Unexpected execution of external commands
* Insecure handling of user-controlled input
* Dependency or supply-chain vulnerabilities
* Exposure of sensitive information
* Authentication or authorization vulnerabilities, if applicable
* Vulnerabilities that could compromise the user's local machine

Because CyberLearn is designed to run locally, vulnerabilities affecting the local application or files on the user's machine are particularly important to report.

---

## What Is Not a Security Vulnerability

The following generally belong in a normal GitHub issue instead:

* UI bugs
* Typographical errors
* Incorrect lesson explanations
* Feature requests
* Missing lessons
* Cosmetic problems
* General documentation improvements
* Performance issues that do not have a security impact

If you're unsure whether something is security-related, treat it cautiously and report it privately.

---

## Responsible Disclosure

Please give maintainers a reasonable opportunity to investigate and address a vulnerability before publicly disclosing technical details.

Security researchers are asked to:

* Avoid accessing data that does not belong to them.
* Avoid modifying or deleting other users' data.
* Avoid disrupting services or systems.
* Avoid testing against systems without authorization.
* Minimize the amount of data accessed during testing.
* Stop testing if unintended access to sensitive information occurs.

Only test systems and files that you own or have explicit permission to test.

---

## Security Updates

When appropriate, security fixes may be documented through:

* GitHub security advisories
* Release notes
* Changelog entries
* Updated documentation

The exact disclosure process may depend on the severity and nature of the vulnerability.

---

## Scope

This security policy applies to the CyberLearn source code and official project distribution.

Third-party software, operating systems, Python installations, GitHub accounts, or other infrastructure outside the project's control may have their own security policies and reporting procedures.

---

## Thank You

Responsible security research helps make open-source software safer.

Thank you for reporting vulnerabilities privately and giving maintainers an opportunity to investigate and fix them.
