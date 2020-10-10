# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added Team checking

### Changed
- Removed :attr:`image_content` from :class:`Image`
- Made :attr:`image_uri` in :class:`Image` required

## [0.3.6] - 2020-10-10
### Added
- Backported OutOfRetriesException from 0.4.0

## [0.3.5] - 2020-10-07
### Dependencies
- Fixed requirements.txt

## [0.3.4] - 2020-10-02
### Fixed
- Fixed a bug on finding the group symbol when all other methods fail

## [0.3.2] - 2020-09-08
### Added
- Added proper logging
- Added support for :class:`babel.Locale`

### Changed
- Updated the regex to match the latest version of the game

### Fixed
- Fixed issues with checking the locale of images.

### Removed
- Removed boilerplate for :class:`Badge`
- Removed boilerplate for :class:`Pokédex`

## [0.3.1] - 2020-06-28
### Changed
- Updated google-cloud-vision to 1.0.0

### Fixed
- Fixed an issue where the OCR might fail the first time. Retries up to 5 times.
- Fixed small issues in the regex strings


## [0.3.0] - 2020-05-20
### Added
- Added Japanese language for :class:`ProfileSelf`
- Added French language for :class:`ProfileSelf`
- Added Korean language for :class:`ProfileSelf`
- Added Chinese (Traditional) language for :class:`ProfileSelf`
- Added Spanish language for :class:`ProfileSelf`
- Added Italian language for :class:`ProfileSelf`
- Added Portuguese (Brazilian) language for :class:`ProfileSelf`

### Changed
- Renamed :attr:`km_walked` to :attr:`travel_km`
- Renamed :attr:`catches` to :attr:`capture_total`
- Renamed :attr:`pokestops` to :attr:`pokestops_visited`
- Renamed :attr:`start_date_text` to :attr:`start_date` and the output from :class:`str` to :class:`datetime.date`

## [0.2.0] - 2020-05-13
### Added
- Added :class:`ProfileSelf` for getting Username (:attr:`username`), Buddy Name (:attr:`buddy_name`)
Distance Walked (:attr:`km_walked`), Pokémon Caught (:attr:`catches`),
PokéStops Visited (:attr:`pokestops`), Total XP (:attr:`total_xp`) and Start Date as text (:attr:`start_date_text`).
This replaces :class:`ProfileTop` and :class:`ProfileBottom`.

### Changed
- :class:`Image` and it's subclasses (:class:`ProfileSelf`) now require a :attr:`service_file`.
This is a :class:`str` to the location of a Google Cloud JSON-key file.


### Removed
- Removed :class:`ProfileTop` in favour of :class:`ProfileSelf`
- Removed :class:`ProfileBottom` in favour of :class:`ProfileSelf`
- Removed Japanese language for :class:`ProfileSelf`
- Removed French language for :class:`ProfileSelf`
- Removed Korean language for :class:`ProfileSelf`
- Removed Chinese (Traditional) language for :class:`ProfileSelf`
- Removed Spanish language for :class:`ProfileSelf`
- Removed Italian language for :class:`ProfileSelf`
- Removed Portuguese (Brazilian) language for :class:`ProfileSelf`

## [0.1.0] - 2010-01-20
### Added
- Bump Version for release
- Added boilerplate for :class:`Badge`
- Added boilerplate for :class:`Pokédex`

## [0.0.2] - 2018-11-04
### Added
- Added Japanese language for :class:`ProfileBottom`
- Added French language for :class:`ProfileBottom`
- Added Korean language for :class:`ProfileBottom`
- Added Chinese (Traditional) language for :class:`ProfileBottom`
- Added Spanish language for :class:`ProfileBottom`
- Added Italian language for :class:`ProfileBottom`
- Added Portuguese (Brazilian) language for :class:`ProfileBottom`

## [0.0.1] - 2018-11-01
### Added
- Added :class:`ProfileTop` for getting Username (:attr:`username`) and Buddy Name (:attr:`buddy_name`)
- Added :class:`ProfileBottom` for getting Total XP (:attr:`total_xp`) and Start Date as text (:attr:`start_date_text`)
- Added English language for :class:`ProfileTop` and :class:`ProfileBottom`

[Unreleased]: https://github.com/TrainerDex/PogoOCR/compare/0.3.5...develop
[0.3.5]: https://github.com/TrainerDex/PogoOCR/compare/0.3.4...0.3.5
[0.3.4]: https://github.com/TrainerDex/PogoOCR/compare/0.3.2...0.3.4
[0.3.2]: https://github.com/TrainerDex/PogoOCR/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/TrainerDex/PogoOCR/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/TrainerDex/PogoOCR/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/TrainerDex/PogoOCR/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/TrainerDex/PogoOCR/compare/0.0.2...0.1.0
[0.0.2]: https://github.com/TrainerDex/PogoOCR/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/TrainerDex/PogoOCR/releases/tag/0.0.1
