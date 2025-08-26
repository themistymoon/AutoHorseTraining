#!/usr/bin/env python3

"""
RACE DECISION LOGIC ANALYSIS

This document explains how the Uma Musume Auto-Train bot decides when to race.

The race decision logic follows a specific priority order in the main execute loop:

=== RACE DECISION FLOW ===

1. **URA FINALE RACE** (Highest Priority)
   - Condition: year == "Finale Season" AND turn == "Race Day"
   - Action: Always races (URA finale is mandatory)
   - Notes: Auto-buys skills if enabled, then races

2. **MANDATORY RACE DAY** (Second Priority)
   - Condition: turn == "Race Day" AND year != "Finale Season"
   - Action: Always races (race day is mandatory)
   - Notes: Auto-buys skills if enabled and not Junior year

3. **MOOD CHECK** (Third Priority)
   - Condition: mood_index < minimum_mood
   - Action: Do recreation instead of racing/training
   - Notes: Low mood prevents both racing and training

4. **CRITERIA-BASED RACING** (Fourth Priority)
   - Conditions:
     * criteria.split(" ")[0] != "criteria" (goal not met)
     * year != "Junior Year Pre-Debut" (not pre-debut)
     * turn < 10 (early in the month)
     * criteria != "Goal Achievedl" (goal not achieved yet)
   - Action: Try to race for goal completion
   - Fallback: If no matching aptitude race found, go to training

5. **G1 RACE PRIORITIZATION** (Fifth Priority)
   - Conditions:
     * state.PRIORITIZE_G1_RACE == True (setting enabled)
     * year_parts[0] != "Junior" (not junior year)
     * len(year_parts) > 3 (valid year format)
     * year_parts[3] not in ["Jul", "Aug"] (not summer break)
   - Action: Search for G1 races every turn
   - Fallback: If no G1 race found, go to training

6. **TRAINING** (Lowest Priority)
   - Condition: All above conditions failed
   - Action: Do training based on selected training logic

=== RACE SELECTION LOGIC ===

When racing is decided, the race selection logic works as follows:

**G1 Race Priority (if prioritize_g1 = True):**
1. Look for G1 races (match_template "g1_race.png")
2. Check if race matches aptitude (match_template "match_track.png")
3. If G1 race with matching aptitude found: race it
4. If no G1 race found: scroll and search more
5. If still no G1 race: return False (fallback to training)

**Regular Race Selection (if prioritize_g1 = False):**
1. Look for any race with matching aptitude ("match_track.png")
2. Click the first matching race found
3. If no matching race: scroll and search more
4. If still no race: return False (fallback to training)

=== CONSECUTIVE RACE CONTROL ===

**Cancel Consecutive Racing (if CANCEL_CONSECUTIVE_RACE = True):**
- If the "cancel" button appears (indicating 3+ consecutive races)
- Cancel the race and return to training
- This prevents over-racing and maintains balance

**Allow Consecutive Racing (if CANCEL_CONSECUTIVE_RACE = False):**
- Click "OK" to continue racing even after 3+ consecutive races
- Prioritizes racing over training safety

=== KEY SETTINGS THAT AFFECT RACING ===

1. **PRIORITIZE_G1_RACE**
   - True: Bot will check for G1 races every turn (except Junior year and summer)
   - False: Bot only races on Race Days or for goal completion

2. **CANCEL_CONSECUTIVE_RACE**
   - True: Bot stops racing after 3 consecutive races
   - False: Bot continues racing regardless of consecutive count

3. **MINIMUM_MOOD**
   - Controls when recreation is prioritized over racing/training
   - Higher values = more recreation, less racing

4. **Training Logic Settings**
   - Only affect training decisions, not race decisions
   - Racing always takes priority over training when conditions are met

=== RACE DECISION PRIORITY SUMMARY ===

Priority Order (Highest to Lowest):
1. URA Finale → Always race
2. Race Day → Always race  
3. Low Mood → Recreation (no race/training)
4. Goal Criteria → Race if goals not met
5. G1 Priority → Race if G1 available (and setting enabled)
6. Training → Default action

The bot strongly prioritizes racing over training when:
- It's a mandatory race day
- Goals need to be completed early in the month
- G1 races are available (if prioritization enabled)
- The character is in good mood

Training only happens when none of the racing conditions are met.
