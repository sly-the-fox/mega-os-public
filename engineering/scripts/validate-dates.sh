#!/usr/bin/env bash
# Scan active state and business files for day+date mismatches.
# Finds patterns like "Thu 2026-03-26" or "Thu Mar 26" and validates
# the day name against `date`. Reports any mismatches.
#
# Exit code: 0 if no mismatches, 1 if mismatches found.
# Designed for daily cron or pre-commit hook use.

set -euo pipefail

MEGA_OS="$(cd "$(dirname "$0")/../.." && pwd)"
ERRORS=0
CHECKED=0

# Map abbreviated day names to full names (as returned by date +%A)
declare -A DAY_FULL=(
    [Mon]=Monday [Tue]=Tuesday [Wed]=Wednesday [Thu]=Thursday
    [Fri]=Friday [Sat]=Saturday [Sun]=Sunday
    [Monday]=Monday [Tuesday]=Tuesday [Wednesday]=Wednesday [Thursday]=Thursday
    [Friday]=Friday [Saturday]=Saturday [Sunday]=Sunday
)

# Month name to number
declare -A MONTH_NUM=(
    [Jan]=01 [Feb]=02 [Mar]=03 [Apr]=04 [May]=05 [Jun]=06
    [Jul]=07 [Aug]=08 [Sep]=09 [Oct]=10 [Nov]=11 [Dec]=12
    [January]=01 [February]=02 [March]=03 [April]=04 [May]=05 [June]=06
    [July]=07 [August]=08 [September]=09 [October]=10 [November]=11 [December]=12
)

# Files to scan
SCAN_DIRS=(
    "$MEGA_OS/active"
    "$MEGA_OS/business/network"
    "$MEGA_OS/core/indexes"
)

check_date() {
    local file="$1"
    local line_num="$2"
    local day_name="$3"
    local date_str="$4"

    local full_day="${DAY_FULL[$day_name]:-}"
    if [[ -z "$full_day" ]]; then
        return
    fi

    local actual_day
    actual_day=$(date -d "$date_str" +%A 2>/dev/null) || return
    CHECKED=$((CHECKED + 1))

    if [[ "$actual_day" != "$full_day" ]]; then
        echo "MISMATCH: $file:$line_num — says '$day_name $date_str' but $date_str is $actual_day"
        ERRORS=$((ERRORS + 1))
    fi
}

for dir in "${SCAN_DIRS[@]}"; do
    [[ -d "$dir" ]] || continue
    while IFS= read -r -d '' file; do
        line_num=0
        while IFS= read -r line; do
            line_num=$((line_num + 1))

            # Pattern 1: "Thu 2026-03-26" or "Thursday 2026-03-26"
            while [[ "$line" =~ (Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[a-z]*[[:space:]]+([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; do
                day="${BASH_REMATCH[1]}"
                dt="${BASH_REMATCH[2]}"
                check_date "$file" "$line_num" "$day" "$dt"
                # Remove match to find more in same line
                line="${line/"${BASH_REMATCH[0]}"/}"
            done

            # Re-read line for pattern 2
            line_num_save=$line_num
            line_num=$line_num_save

            # Pattern 2: "Thu Mar 26" — need to infer year (use current year)
            year=$(date +%Y)
            orig_line="$line"
            while [[ "$orig_line" =~ (Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[a-z]*[[:space:]]+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[[:space:]]+([0-9]{1,2}) ]]; do
                day="${BASH_REMATCH[1]}"
                month="${BASH_REMATCH[2]}"
                day_of_month="${BASH_REMATCH[3]}"
                month_num="${MONTH_NUM[${month:0:3}]:-}"
                if [[ -n "$month_num" ]]; then
                    iso_date="$year-$month_num-$(printf '%02d' "$day_of_month")"
                    check_date "$file" "$line_num" "$day" "$iso_date"
                fi
                orig_line="${orig_line/"${BASH_REMATCH[0]}"/}"
            done

        done < "$file"
    done < <(find "$dir" -maxdepth 1 -name '*.md' -print0 2>/dev/null)
done

echo ""
echo "Date validation complete: $CHECKED dates checked, $ERRORS mismatches found."

if [[ $ERRORS -gt 0 ]]; then
    exit 1
else
    exit 0
fi
