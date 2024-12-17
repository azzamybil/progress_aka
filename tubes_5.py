import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt

class AlgorithmAnalyzer:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Hotel Rating Algorithm Analyzer")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f4f9')
        self.root.resizable(False, False)

    def create_widgets(self):
        self.create_header()
        self.create_input_frame()
        self.create_result_display()
        self.create_footer()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame, 
            text="Hotel Rating Algorithm Analyzer", 
            font=("Arial", 16, "bold"), 
            fg='white', 
            bg='#2c3e50'
        )
        header_label.pack(expand=True)

    def create_input_frame(self):
        input_frame = tk.Frame(self.root, bg='#f0f4f9')
        input_frame.pack(pady=20, padx=20, fill='x')

        input_label = tk.Label(
            input_frame, 
            text="Enter Hotel Names and Ratings (comma-separated, e.g. 'Hotel A 4.5, Hotel B 3.8'):", 
            font=("Arial", 10), 
            bg='#f0f4f9'
        )
        input_label.pack(anchor='w')

        self.input_entry = tk.Entry(
            input_frame, 
            font=("Courier", 10), 
            width=70,
            bd=2,
            relief='groove'
        )
        self.input_entry.pack(fill='x', pady=5)
        self.input_entry.insert(0, "bw luxury 7, swiss bellhotel 8")

        analyze_btn = tk.Button(
            input_frame, 
            text="Analyze Hotels", 
            command=self.analyze_algorithms,
            bg='#3498db', 
            fg='white', 
            font=("Arial", 10, "bold")
        )
        analyze_btn.pack(pady=10)

    def create_result_display(self):
        result_frame = tk.Frame(self.root)
        result_frame.pack(padx=20, pady=10, fill='both', expand=True)

        self.result_text = tk.Text(
            result_frame, 
            font=("Courier", 10), 
            wrap=tk.WORD,
            bd=2,
            relief='sunken',
            height=20
        )
        self.result_text.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)

    def create_footer(self):
        footer = tk.Label(
            self.root, 
            text="\u00a9 2024 Hotel Rating Analyzer", 
            font=("Arial", 8), 
            fg='gray',
            bg='#f0f4f9'
        )
        footer.pack(side='bottom', pady=10)

    def iterative_average(self, ratings):
        return sum(ratings) / len(ratings)

    def recursive_average(self, ratings, n):
        if n == 1:
            return ratings[0]
        return (ratings[n-1] + (n-1) * self.recursive_average(ratings, n-1)) / n

    def bubble_sort(self, arr):
        n = len(arr)
        arr_copy = arr.copy()
        for i in range(n):
            for j in range(0, n-i-1):
                if arr_copy[j][1] > arr_copy[j+1][1]:  # Compare based on rating
                    arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
        return arr_copy

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i][1] <= right[j][1]:  # Compare based on rating
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def visualize_results(self, times):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # Plot for iterative and recursive averages
        axs[0].bar(['Iterative Avg', 'Recursive Avg'], times[:2], color=['blue', 'orange'])
        axs[0].set_ylabel('Execution Time (µs)')
        axs[0].set_title('Average Calculation Times')

        # Plot for sorting algorithms
        axs[1].bar(['Bubble Sort', 'Merge Sort'], times[2:], color=['green', 'red'])
        axs[1].set_ylabel('Execution Time (µs)')
        axs[1].set_title('Sorting Algorithm Times')

        plt.tight_layout()
        plt.show()

    def analyze_algorithms(self):
        try:
            self.result_text.delete(1.0, tk.END)
            hotel_data = self.input_entry.get().split(',')
            hotel_names = []
            ratings = []

            # Parsing the input and creating a list of tuples (hotel_name, rating)
            for item in hotel_data:
                name, rating = item.rsplit(' ', 1)
                hotel_names.append(name.strip())
                ratings.append((name.strip(), float(rating.strip())))

            input_count = len(ratings)
            results = [f"Jumlah Input: {input_count}\n"]

            start = time.perf_counter()
            avg_iter = self.iterative_average([rating[1] for rating in ratings])  # Average based on ratings
            iter_time = time.perf_counter() - start
            results.append(f"Iterative Average: {avg_iter:.4f}")
            results.append(f"Iterative Time: {iter_time*1e6:.4f} µs\n")

            start = time.perf_counter()
            avg_recur = self.recursive_average([rating[1] for rating in ratings], len(ratings))
            recur_time = time.perf_counter() - start
            results.append(f"Recursive Average: {avg_recur:.4f}")
            results.append(f"Recursive Time: {recur_time*1e6:.4f} µs\n")

            # Sorting algorithms
            start = time.perf_counter()
            bubble_sorted = self.bubble_sort(ratings)
            bubble_time = time.perf_counter() - start
            results.append(f"Bubble Sort Time: {bubble_time*1e6:.4f} µs")
            results.append(f"Bubble Sorted: {', '.join([f'{name} {rating}' for name, rating in bubble_sorted])}\n")

            start = time.perf_counter()
            merge_sorted = self.merge_sort(ratings)
            merge_time = time.perf_counter() - start
            results.append(f"Merge Sort Time: {merge_time*1e6:.4f} µs")
            results.append(f"Merge Sorted: {', '.join([f'{name} {rating}' for name, rating in merge_sorted])}\n")

            for result in results:
                self.result_text.insert(tk.END, result + "\n")

            self.visualize_results([iter_time*1e6, recur_time*1e6, bubble_time*1e6, merge_time*1e6])

        except Exception as e:
            messagebox.showerror("Error", f"Invalid Input: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmAnalyzer(root)
    root.mainloop()
