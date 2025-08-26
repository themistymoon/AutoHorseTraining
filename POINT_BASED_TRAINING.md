# Point-Based Training System

## Overview
The new point-based training system provides sophisticated training logic with supporter recognition and mood optimization.

## Features

### Point Calculation System
- **Base training**: 2 points for any available training
- **Regular supporters**: 1 point each (included in base)
- **Kitasan Black**: 1.5 points (0.5 bonus)
- **Exclamation mark supporters**: 1.5 points (0.5 bonus)
- **Director/Otonashi**: 0.5 points (-0.5 penalty)
- **Speed/Wit training**: +0.5 bonus for main stats
- **Rainbow supporters**: 
  - 1 matching rainbow: +2 points
  - 2+ matching rainbow: +5 points

### Mood-Based Recreation Logic
- If best training < 2.5 points and mood isn't GREAT: Do recreation instead
- Recreation provides 20% stat bonus when mood improves

### Image Recognition
The system uses image recognition to detect special supporters:
- `game_assets/icons/kitasan.png` - Kitasan Black supporter
- `game_assets/icons/exclamation_mark.png` - Exclamation mark supporters
- `game_assets/icons/director.png` - Director supporter
- `game_assets/icons/otonashi.png` - Otonashi supporter

## GUI Integration
Available in the overlay GUI under "Training Logic" dropdown as "point_based" option.

## Example Calculation
For SPD training with 2 rainbow speed supporters:
- Base: 2 points
- Main stat bonus: +0.5 points
- Rainbow bonus (2 matching): +5 points
- **Total: 7.5 points**

## Error Handling
- Validates data structure integrity
- Safe handling of missing or invalid supporter data
- Graceful fallback for image recognition failures
- Comprehensive logging for debugging

## Status
✅ Fully implemented and tested
✅ GUI integration complete
✅ Error handling robust
✅ Image recognition working
✅ Recreation logic functional
