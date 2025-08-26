# Point-Based Training Logic Documentation

## Overview
The point-based training logic is an advanced scoring system that evaluates training options based on supporter quality, special supporter recognition, stat priorities, and mood optimization.

## Scoring System

### Base Points
- **1.0 point** per regular supporter in training

### Special Supporter Bonuses
- **Kitasan Black**: 1.5 points (0.5 bonus)
- **Exclamation Mark Supporters**: 1.5 points (0.5 bonus)
- **Director**: 0.5 points (-0.5 penalty)
- **Otonashi**: 0.5 points (-0.5 penalty)

### Stat Priority Bonuses
- **Speed (SPD) Training**: +0.5 points
- **Wit (WIT) Training**: +0.5 points

### Rainbow Supporter System
- **1 Rainbow Supporter**: +1.0 bonus (2.0 total for that supporter)
- **2+ Rainbow Supporters**: +4.0 bonus (5.0 total for rainbow supporters)

## Mood-Based Recreation Logic

### Recreation Conditions
The system will choose recreation over training when:
1. **Best training points < 3.0** AND
2. **Current mood ≠ "GREAT"**

### Reasoning
- GREAT mood provides 20% bonus to training stat gains
- Low point training (< 3.0) with non-GREAT mood is inefficient
- Recreation improves mood for better future training

## Point Calculation Examples

### Example 1: High-Value Speed Training
```
SPD Training:
- 3 regular supporters = 3.0 points
- Speed training bonus = +0.5 points  
- 2 rainbow supporters = +4.0 points
Total: 7.5 points → Train SPD
```

### Example 2: Moderate Training with Mood Check
```
STA Training:
- 2 regular supporters = 2.0 points
- 1 exclamation supporter = +0.5 points
Total: 2.5 points

If mood ≠ GREAT → Recreation (wait for mood bonus)
If mood = GREAT → Train STA
```

### Example 3: Mixed Quality Supporters
```
WIT Training:
- 4 regular supporters = 4.0 points
- Wit training bonus = +0.5 points
- 1 rainbow supporter = +1.0 points
- 1 director present = -0.5 points
Total: 5.0 points → Train WIT
```

## Image Recognition Assets

The following supporter images are used for detection:
- `game_assets/icons/kitasan.png` - Kitasan Black supporter
- `game_assets/icons/exclamation_mark.png` - Exclamation mark supporters  
- `game_assets/icons/director.png` - Director supporter
- `game_assets/icons/otonashi.png` - Otonashi supporter

## Integration

### GUI Selection
Available in Training Logic dropdown as "point_based"

### Return Values
- **Stat name** (e.g., "SPD", "STA"): Do that training
- **"recreation"**: Do recreation instead of training
- **None**: Rest (no safe training available)

## Strategy Benefits

1. **Maximizes Training Efficiency**: Prioritizes high-value training combinations
2. **Mood Optimization**: Waits for GREAT mood when training value is marginal
3. **Supporter Recognition**: Accounts for special supporter values automatically
4. **Stat Priority**: Emphasizes Speed and Wit as main stats
5. **Rainbow Synergy**: Heavily rewards rainbow supporter combinations

## Usage Recommendations

- **Best for**: Players who want maximum training efficiency
- **Requires**: Proper supporter image assets in game_assets/icons/
- **Mood Dependency**: Works best when mood can be reliably detected
- **Safe Training**: Still respects failure rate limits like other logics

This logic provides the most sophisticated training decision-making in the bot, combining multiple factors for optimal stat development.
