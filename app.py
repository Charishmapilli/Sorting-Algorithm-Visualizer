from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def make_step(
    array,
    action,
    explanation,
    pseudo,
    comparisons=0,
    swaps=0,
    active_indices=None
):
    return {
        "array": array.copy(),
        "action": action,
        "explanation": explanation,
        "pseudo": pseudo,
        "comparisons": comparisons,
        "swaps": swaps,
        "active_indices": active_indices or []
    }


# =========================================================
# BUBBLE SORT
# =========================================================

def bubble_sort_steps(original):
    arr = original.copy()
    steps = []

    steps.append(
        make_step(
            arr,
            "START",
            "Start Bubble Sort",
            1
        )
    )

    total_comparisons = 0
    total_swaps = 0

    n = len(arr)

    for i in range(n - 1):

        for j in range(n - i - 1):

            a = arr[j]
            b = arr[j + 1]

            total_comparisons += 1

            steps.append(
                make_step(
                    arr,
                    "COMPARE",
                    f"Compare {a} and {b}",
                    5,
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    active_indices=[j, j + 1]
                )
            )

            if arr[j] > arr[j + 1]:

                steps.append(
                    make_step(
                        arr,
                        "SWAP",
                        f"Swap {a} and {b}",
                        7,
                        comparisons=total_comparisons,
                        swaps=total_swaps + 1,
                        active_indices=[j, j + 1]
                    )
                )

                arr[j], arr[j + 1] = arr[j + 1], arr[j]

                total_swaps += 1

            else:

                steps.append(
                    make_step(
                        arr,
                        "NO SWAP",
                        f"No Swap: {a} and {b}",
                        6,
                        comparisons=total_comparisons,
                        swaps=total_swaps,
                        active_indices=[j, j + 1]
                    )
                )

    steps.append(
        make_step(
            arr,
            "COMPLETED",
            "Sorting completed",
            11,
            comparisons=total_comparisons,
            swaps=total_swaps
        )
    )

    return steps


# =========================================================
# INSERTION SORT
# =========================================================

def insertion_sort_steps(original):
    arr = original.copy()
    steps = []

    steps.append(
        make_step(
            arr,
            "START",
            "Start Insertion Sort",
            1
        )
    )

    total_comparisons = 0
    total_shifts = 0

    for i in range(1, len(arr)):

        key = arr[i]

        steps.append(
            make_step(
                arr,
                "SELECT KEY",
                f"Select key {key}",
                4,
                comparisons=total_comparisons,
                swaps=total_shifts,
                active_indices=[i]
            )
        )

        j = i - 1

        while j >= 0:

            total_comparisons += 1

            steps.append(
                make_step(
                    arr,
                    "COMPARE",
                    f"Compare {arr[j]} and {key}",
                    6,
                    comparisons=total_comparisons,
                    swaps=total_shifts,
                    active_indices=[j, j + 1]
                )
            )

            if arr[j] > key:

                value = arr[j]

                arr[j + 1] = arr[j]

                total_shifts += 1

                steps.append(
                    make_step(
                        arr,
                        "SHIFT RIGHT",
                        f"Shift {value} to the right",
                        7,
                        comparisons=total_comparisons,
                        swaps=total_shifts,
                        active_indices=[j, j + 1]
                    )
                )

                j -= 1

            else:
                break

        arr[j + 1] = key

        steps.append(
            make_step(
                arr,
                "INSERT KEY",
                f"Insert key {key}",
                10,
                comparisons=total_comparisons,
                swaps=total_shifts,
                active_indices=[j + 1]
            )
        )

    steps.append(
        make_step(
            arr,
            "COMPLETED",
            "Sorting completed",
            12,
            comparisons=total_comparisons,
            swaps=total_shifts
        )
    )

    return steps


# =========================================================
# SELECTION SORT
# =========================================================

def selection_sort_steps(original):
    arr = original.copy()
    steps = []

    steps.append(
        make_step(
            arr,
            "START",
            "Start Selection Sort",
            1
        )
    )

    total_comparisons = 0
    total_swaps = 0

    n = len(arr)

    for i in range(n - 1):

        min_index = i

        steps.append(
            make_step(
                arr,
                "SET MINIMUM",
                f"Set minimum {arr[min_index]}",
                4,
                comparisons=total_comparisons,
                swaps=total_swaps,
                active_indices=[min_index]
            )
        )

        for j in range(i + 1, n):

            total_comparisons += 1

            steps.append(
                make_step(
                    arr,
                    "COMPARE",
                    f"Compare {arr[j]} and {arr[min_index]}",
                    6,
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    active_indices=[j, min_index]
                )
            )

            if arr[j] < arr[min_index]:

                min_index = j

                steps.append(
                    make_step(
                        arr,
                        "NEW MINIMUM",
                        f"New minimum {arr[min_index]}",
                        8,
                        comparisons=total_comparisons,
                        swaps=total_swaps,
                        active_indices=[min_index]
                    )
                )

        if min_index != i:

            a = arr[i]
            b = arr[min_index]

            steps.append(
                make_step(
                    arr,
                    "SWAP",
                    f"Swap {a} and {b}",
                    11,
                    comparisons=total_comparisons,
                    swaps=total_swaps + 1,
                    active_indices=[i, min_index]
                )
            )

            arr[i], arr[min_index] = arr[min_index], arr[i]

            total_swaps += 1

    steps.append(
        make_step(
            arr,
            "COMPLETED",
            "Sorting completed",
            13,
            comparisons=total_comparisons,
            swaps=total_swaps
        )
    )

    return steps


# =========================================================
# QUICK SORT
# =========================================================

def quick_sort_steps(original):
    arr = original.copy()
    steps = []

    total_comparisons = 0
    total_swaps = 0

    steps.append(
        make_step(
            arr,
            "START",
            "Start Quick Sort",
            1
        )
    )

    def partition(low, high):

        nonlocal total_comparisons
        nonlocal total_swaps

        pivot = arr[high]

        steps.append(
            make_step(
                arr,
                "CHOOSE PIVOT",
                f"Choose pivot {pivot}",
                2,
                comparisons=total_comparisons,
                swaps=total_swaps,
                active_indices=[high]
            )
        )

        i = low - 1

        for j in range(low, high):

            total_comparisons += 1

            steps.append(
                make_step(
                    arr,
                    "COMPARE",
                    f"Compare {arr[j]} and pivot {pivot}",
                    5,
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    active_indices=[j, high]
                )
            )

            if arr[j] < pivot:

                i += 1

                if i != j:

                    a = arr[i]
                    b = arr[j]

                    arr[i], arr[j] = arr[j], arr[i]

                    total_swaps += 1

                    steps.append(
                        make_step(
                            arr,
                            "SWAP",
                            f"Swap {a} and {b}",
                            8,
                            comparisons=total_comparisons,
                            swaps=total_swaps,
                            active_indices=[i, j]
                        )
                    )

        pivot_value = arr[high]

        if i + 1 != high:

            other = arr[i + 1]

            arr[i + 1], arr[high] = arr[high], arr[i + 1]

            total_swaps += 1

            steps.append(
                make_step(
                    arr,
                    "PLACE PIVOT",
                    f"Place pivot {pivot_value}",
                    12,
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    active_indices=[i + 1]
                )
            )

        else:

            steps.append(
                make_step(
                    arr,
                    "PLACE PIVOT",
                    f"Place pivot {pivot_value}",
                    12,
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    active_indices=[i + 1]
                )
            )

        return i + 1

    def quick_sort(low, high):

        if low < high:

            pivot_index = partition(low, high)

            if low < pivot_index - 1:

                steps.append(
                    make_step(
                        arr,
                        "LEFT PART",
                        "Sort left part",
                        13,
                        comparisons=total_comparisons,
                        swaps=total_swaps,
                        active_indices=list(
                            range(low, pivot_index)
                        )
                    )
                )

                quick_sort(low, pivot_index - 1)

            if pivot_index + 1 < high:

                steps.append(
                    make_step(
                        arr,
                        "RIGHT PART",
                        "Sort right part",
                        14,
                        comparisons=total_comparisons,
                        swaps=total_swaps,
                        active_indices=list(
                            range(pivot_index + 1, high + 1)
                        )
                    )
                )

                quick_sort(pivot_index + 1, high)

    quick_sort(0, len(arr) - 1)

    steps.append(
        make_step(
            arr,
            "COMPLETED",
            "Sorting completed",
            15,
            comparisons=total_comparisons,
            swaps=total_swaps
        )
    )

    return steps


# =========================================================
# MERGE SORT
# =========================================================

def merge_sort_steps(original):
    arr = original.copy()
    steps = []

    total_comparisons = 0

    steps.append(
        make_step(
            arr,
            "START",
            "Start Merge Sort",
            1
        )
    )

    def merge(low, mid, high):

        nonlocal total_comparisons

        left = arr[low:mid + 1]
        right = arr[mid + 1:high + 1]

        i = 0
        j = 0
        k = low

        while i < len(left) and j < len(right):

            total_comparisons += 1

            steps.append(
                make_step(
                    arr,
                    "COMPARE",
                    f"Compare {left[i]} and {right[j]}",
                    7,
                    comparisons=total_comparisons,
                    swaps=0,
                    active_indices=[k]
                )
            )

            if left[i] <= right[j]:

                value = left[i]
                arr[k] = value
                i += 1

            else:

                value = right[j]
                arr[k] = value
                j += 1

            steps.append(
                make_step(
                    arr,
                    "PLACE ELEMENT",
                    f"Place {value}",
                    8,
                    comparisons=total_comparisons,
                    swaps=0,
                    active_indices=[k]
                )
            )

            k += 1

        while i < len(left):

            value = left[i]
            arr[k] = value

            steps.append(
                make_step(
                    arr,
                    "COPY REMAINING",
                    f"Copy {value}",
                    9,
                    comparisons=total_comparisons,
                    swaps=0,
                    active_indices=[k]
                )
            )

            i += 1
            k += 1

        while j < len(right):

            value = right[j]
            arr[k] = value

            steps.append(
                make_step(
                    arr,
                    "COPY REMAINING",
                    f"Copy {value}",
                    9,
                    comparisons=total_comparisons,
                    swaps=0,
                    active_indices=[k]
                )
            )

            j += 1
            k += 1

        steps.append(
            make_step(
                arr,
                "MERGE COMPLETE",
                "Merge complete",
                10,
                comparisons=total_comparisons,
                swaps=0,
                active_indices=list(
                    range(low, high + 1)
                )
            )
        )

    def merge_sort(low, high):

        if low >= high:
            return

        mid = (low + high) // 2

        steps.append(
            make_step(
                arr,
                "DIVIDE",
                "Divide array",
                4,
                comparisons=total_comparisons,
                swaps=0,
                active_indices=list(
                    range(low, high + 1)
                )
            )
        )

        merge_sort(low, mid)
        merge_sort(mid + 1, high)

        merge(low, mid, high)

    merge_sort(0, len(arr) - 1)

    steps.append(
        make_step(
            arr,
            "COMPLETED",
            "Sorting completed",
            12,
            comparisons=total_comparisons,
            swaps=0
        )
    )

    return steps


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/steps", methods=["POST"])
def get_steps():

    data = request.get_json()

    algorithm = data.get("algorithm")
    array = data.get("array")

    if not isinstance(array, list):
        return jsonify({
            "error": "Invalid array"
        }), 400

    if len(array) < 2:
        return jsonify({
            "error": "Enter at least 2 numbers"
        }), 400

    try:
        array = [int(x) for x in array]
    except:
        return jsonify({
            "error": "Please enter valid numbers"
        }), 400

    if algorithm == "bubble":
        steps = bubble_sort_steps(array)

    elif algorithm == "insertion":
        steps = insertion_sort_steps(array)

    elif algorithm == "selection":
        steps = selection_sort_steps(array)

    elif algorithm == "quick":
        steps = quick_sort_steps(array)

    elif algorithm == "merge":
        steps = merge_sort_steps(array)

    else:
        return jsonify({
            "error": "Invalid algorithm"
        }), 400

    return jsonify({
        "algorithm": algorithm,
        "steps": steps
    })


if __name__ == "__main__":
    app.run(debug=True)