# Changelog

## v1.1.0 - Visual and Performance Upgrade (2025-04-20)

### Added
- Sprite-based graphics for all game elements
  - Classic Space Invaders sprites for aliens (3 types)
  - Spaceship sprite for player
  - Enhanced bullet visuals with distinctive designs
- Sprite management system with caching
- CLI-based Prolog bridge for cross-platform compatibility
- Ultra-smooth player movement with subframe updates
- Enhanced bullet visuals with trailing effects
- Game controls information display

### Changed
- Completely overhauled movement system with dual update rates
  - Player moves at 60fps with subframe precision
  - Aliens maintain classic frame-by-frame movement
- Improved collision detection with proper sprite boundaries
- Enhanced player shooting mechanics with faster, more responsive bullets
- Simplified UI removing strategy color references
- Updated README with latest features and improvements
- Adjusted game speed for better playability

### Fixed
- Compatibility issues with PySwip on macOS (especially Apple Silicon)
- Player movement lag and unresponsiveness
- Inconsistent player speed between different game states
- Missing graphics and placeholder rectangles
- Various small gameplay bugs and visual glitches

## v1.0.0 - Initial Release (2025-04-15)

### Added
- Classic Space Invaders gameplay
- Prolog-driven AI for aliens with PySwip integration
- Row-based strategy system with 5 distinct strategies
- Game state management (menu, playing, game over)
- Lives system and scoring
- Destructible barriers
- Basic rectangle-based graphics
- Collision detection
- Win and lose conditions 