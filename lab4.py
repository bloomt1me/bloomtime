import itertools

items = {
    'r': {'size': 3, 'points': 25},
    'p': {'size': 2, 'points': 15},
    'a': {'size': 2, 'points': 15},
    'm': {'size': 2, 'points': 20},
    'i': {'size': 1, 'points': 5},
    'k': {'size': 1, 'points': 15},
    'x': {'size': 3, 'points': 20},
    't': {'size': 1, 'points': 25},
    'f': {'size': 1, 'points': 15},
    'd': {'size': 1, 'points': 10},
    's': {'size': 2, 'points': 20},
    'c': {'size': 2, 'points': 20}
}

TOTAL_PENALTY = sum(items[item]['points'] for item in items)

def calculate_score_fast(selected_items, initial_points):
    """Fast calculation of survival points"""
    selected_points = sum(items[item]['points'] for item in selected_items)
    return initial_points + 2 * selected_points - TOTAL_PENALTY

def get_total_size(selected_items):
    """Calculate total size of selected items"""
    return sum(items[item]['size'] for item in selected_items)

def arrange_in_grid(selected_items, rows, cols):
    """Arrange selected items in a grid"""
    grid = [['[ ]'] * cols for _ in range(rows)]

    item_positions = []
    for item in selected_items:
        size = items[item]['size']
        for _ in range(size):
            item_positions.append(item)
    
    index = 0
    for i in range(rows):
        for j in range(cols):
            if index < len(item_positions):
                grid[i][j] = f'[{item_positions[index]}]'
                index += 1
    
    return grid

def find_all_valid_combinations(backpack_size, initial_points, required_items=None):
    """Find all valid item combinations"""
    if required_items is None:
        required_items = []
    
    valid_combinations = []
    all_items = list(items.keys())
    
    for r in range(0, len(all_items) + 1):
        for combination in itertools.combinations(all_items, r):
            valid = all(item in combination for item in required_items)
            if not valid:
                continue
            
            total_size = get_total_size(combination)
            
            if total_size <= backpack_size:
                score = calculate_score_fast(combination, initial_points)
                
                if score > 0:
                    valid_combinations.append({
                        'items': combination,
                        'score': score,
                        'size': total_size,
                        'used_space_percent': total_size / backpack_size * 100
                    })
    
    valid_combinations.sort(key=lambda x: x['score'], reverse=True)
    return valid_combinations

def analyze_7_slots():
    """Analyze the 7-slot backpack case"""
    print("=" * 60)
    print("Analyzing 7-slot backpack case")
    print("=" * 60)
    
    combinations_7 = find_all_valid_combinations(7, INITIAL_POINTS)
    
    if combinations_7:
        print(f"Found {len(combinations_7)} valid combinations")
        print("\nAll valid combinations for 7-slot backpack:")
        for i, combo in enumerate(combinations_7):
            print(f"\nCombination {i+1}:")
            print(f"Items: {combo['items']}")
            print(f"Total size: {combo['size']}/7 ({combo['used_space_percent']:.1f}%)")
            print(f"Survival points: {combo['score']}")
            
            if combo['size'] <= 8:
                grid = arrange_in_grid(combo['items'], 2, 4)
                print("Backpack layout (2x4):")
                for row in grid:
                    print(" ".join(row))
            else:
                grid = arrange_in_grid(combo['items'], 3, 3)
                print("Backpack layout (3x3):")
                for row in grid:
                    print(" ".join(row))
    else:
        print("❌ No valid item combinations found for 7-slot backpack")
        print("\nReason analysis:")
        
        best_combo = []
        best_score = -float('inf')
        for r in range(1, len(items) + 1):
            for combination in itertools.combinations(items.keys(), r):
                if get_total_size(combination) <= 7:
                    score = calculate_score_fast(combination, INITIAL_POINTS)
                    if score > best_score:
                        best_score = score
                        best_combo = combination
        
        print(f"\nBest combination for 7-slot backpack: {best_combo}")
        print(f"Best score: {best_score}")
        print(f"Total size: {get_total_size(best_combo)}/7")
        
        if best_score <= 0:
            print("✅ Proof: 7-slot backpack cannot achieve positive survival points, solution does not exist")

def analyze_variant_4():
    """Analyze variant 4 case (9-slot backpack)"""
    print("\n" + "=" * 60)
    print("Analyzing Variant 4: 3x3 backpack (9 slots), no disease requirements, initial 15 points")
    print("=" * 60)
    
    combinations_9 = find_all_valid_combinations(9, 15)
    
    if combinations_9:
        print(f"Found {len(combinations_9)} valid combinations")
        
        best_score = combinations_9[0]['score']
        worst_score = combinations_9[-1]['score']
        avg_score = sum(c['score'] for c in combinations_9) / len(combinations_9)
        
        print(f"\nStatistics:")
        print(f"Highest score: {best_score}")
        print(f"Lowest score: {worst_score}")
        print(f"Average score: {avg_score:.1f}")
        
        print(f"\nTop 10 combinations with backpack layouts:")
        for i, combo in enumerate(combinations_9[:10]):
            print(f"\nCombination {i+1} (Score: {combo['score']}):")
            print(f"Items: {sorted(combo['items'])}")
            print(f"Total size: {combo['size']}/9 ({combo['used_space_percent']:.1f}%)")
            
            grid = arrange_in_grid(combo['items'], 3, 3)
            print("Backpack layout:")
            for row in grid:
                print(" ".join(row))
    
    return combinations_9

def find_unique_combinations():
    """Find and display unique combinations without duplicates"""
    print("\n" + "=" * 60)
    print("Finding all unique item combinations")
    print("=" * 60)
    
    backpack_sizes = [7, 9]
    
    for size in backpack_sizes:
        print(f"\n{'='*40}")
        print(f"Backpack size: {size} slots")
        print(f"{'='*40}")
        
        combinations = find_all_valid_combinations(size, 15)
        
        if combinations:
            print(f"Found {len(combinations)} unique valid combinations:")
            
            for i, combo in enumerate(combinations):
                items_str = str(sorted(combo['items']))
                print(f"{i+1:2d}. Items: {items_str:30} | Size: {combo['size']:2d}/{size} | Score: {combo['score']:3d}")
        else:
            print("No valid combinations found")
            
            best_combo = []
            best_score = -float('inf')
            for r in range(1, len(items) + 1):
                for combination in itertools.combinations(items.keys(), r):
                    if get_total_size(combination) <= size:
                        score = calculate_score_fast(combination, 15)
                        if score > best_score:
                            best_score = score
                            best_combo = combination
            
            print(f"Best possible combination: {sorted(best_combo)}")
            print(f"Best possible score: {best_score}")
            print(f"Total size: {get_total_size(best_combo)}/{size}")

def main():
    global INITIAL_POINTS
    INITIAL_POINTS = 15
    
    print("BACKPACK OPTIMIZATION PROBLEM")
    print("Each item can only be taken once (no duplicates)")
    print("=" * 60)
    
    analyze_7_slots()
    
    combinations_9 = analyze_variant_4()
    
    find_unique_combinations()
    
    with open('backpack_solutions.txt', 'w', encoding='utf-8') as f:
        f.write("Backpack Problem Solution Analysis\n")
        f.write("Each item can only be taken once (no duplicates)\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("1. 7-slot backpack analysis:\n")
        combinations_7 = find_all_valid_combinations(7, INITIAL_POINTS)
        if combinations_7:
            f.write(f"Found {len(combinations_7)} valid combinations\n")
            for i, combo in enumerate(combinations_7):
                f.write(f"   Combination {i+1}: {sorted(combo['items'])} | Size: {combo['size']}/7 | Score: {combo['score']}\n")
        else:
            f.write("❌ No valid solutions found for 7-slot backpack\n")
        
        f.write("\n2. Variant 4 (9-slot backpack) analysis:\n")
        if combinations_9:
            f.write(f"Found {len(combinations_9)} valid combinations\n")
            for i, combo in enumerate(combinations_9):
                f.write(f"   Combination {i+1}: {sorted(combo['items'])} | Size: {combo['size']}/9 | Score: {combo['score']}\n")

if __name__ == "__main__":
    main()