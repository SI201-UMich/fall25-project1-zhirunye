"""
111_final_penguins.py

Author: Zhirun Ye
Course: SI 201 - Project 1
Dataset: Palmer Penguins (penguins.csv)

GenAI usage declaration:

This file was created with assistance from ChatGPT to help overcome specific 
programming challenges in the following areas:

1. CSV File Processing with Unnamed Columns: I was uncertain how to properly 
   handle the unnamed index column (first column with empty header) in the CSV file. 
   ChatGPT provided a template for detecting and skipping empty header columns using 
   conditional checks on fieldnames. I adapted this approach but simplified it to 
   match our course level by removing complex type annotations.

2. Data Preprocessing for NA Values: I needed help handling "NA" values and 
   empty strings in numeric conversion. ChatGPT showed me the technique of checking 
   for "NA" strings and empty values before attempting conversion. I implemented 
   this in the data cleaning functions.

3. unittest Framework Implementation: While I understood basic assertion testing, 
   I was unfamiliar with Python's unittest framework structure (test classes, 
   setUp methods, assert methods). ChatGPT provided examples of unittest test cases 
   that I studied and then rewrote to test our specific analysis functions with 
   appropriate test method names and assertions.

4. Column Name Validation: I was checking for column name variations that don't 
   exist in the actual dataset. ChatGPT helped me understand how to validate column 
   names against the actual data structure, which led to fixing the column name 
   checks in the analysis functions.

Specific AI-generated code segments I adapted:
- The basic unittest class structure with test methods
- The logic for handling unnamed CSV columns in import_csv_data()
- The approach for checking "NA" values in data preprocessing

All AI-assisted code was reviewed, understood, and modified to:
- Remove advanced Python features (type annotations, complex generics)
- Use only concepts covered in SI 201 curriculum
- Ensure code matches our course coding standards and simplicity requirements
- Focus on data-oriented programming principles taught in class
"""

import csv
import sys
import unittest

def import_csv_data(file_path, encoding="utf-8"):
    """
    Read CSV into a list of dictionaries, clean header names, strip whitespace,
    drop completely empty rows, and convert numeric-like fields to numbers.
    """
    rows = []
    try:
        with open(file_path, "r", encoding=encoding, newline='') as f:
            reader = csv.DictReader(f)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn.strip() if fn is not None else "" for fn in raw_fieldnames]
            
            if fieldnames and fieldnames[0] == "":
                for raw_row in reader:
                    cleaned_row = {}
                    for k, v in raw_row.items():
                        if k is None:
                            continue
                        k_clean = k.strip()
                        if k_clean == "":
                            continue
                        if isinstance(v, str):
                            v2 = v.strip()
                        else:
                            v2 = v
                        cleaned_row[k_clean] = v2
                    if any(val not in (None, "") for val in cleaned_row.values()):
                        rows.append(_convert_row_types(cleaned_row))
            else:
                for raw_row in reader:
                    cleaned_row = {}
                    for k, v in raw_row.items():
                        if k is None:
                            continue
                        k_clean = k.strip()
                        if isinstance(v, str):
                            v2 = v.strip()
                        else:
                            v2 = v
                        cleaned_row[k_clean] = v2
                    if any(val not in (None, "") for val in cleaned_row.values()):
                        rows.append(_convert_row_types(cleaned_row))
        return rows
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return []

def _convert_row_types(row):
    """
    Try to convert values in the row to numbers where appropriate.
    """
    out = {}
    for k, v in row.items():
        if v is None or v == "" or v == "NA":
            out[k] = ""
            continue
        s = str(v).replace(",", "")
        s_stripped = s.strip()
        if s_stripped == "" or s_stripped == "NA":
            out[k] = ""
            continue
        try:
            if "." not in s_stripped:
                i = int(s_stripped)
                out[k] = i
                continue
        except Exception:
            pass
        try:
            f = float(s_stripped)
            out[k] = f
            continue
        except Exception:
            out[k] = v
    return out

def analyze_dataset(data):
    """
    Return simple dataset summary.
    """
    if not data:
        return {"error": "empty dataset"}
    variables = list(data[0].keys())
    sample_entry = data[0]
    row_count = len(data)
    return {"variables": variables, "sample_entry": sample_entry, "row_count": row_count}

def display_analysis_results(results):
    """Nicely print dataset summary produced by analyze_dataset()."""
    if not results:
        print("No results to display.")
        return
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    print("=== Dataset summary ===")
    print("Variables (columns):")
    for i, v in enumerate(results["variables"], 1):
        print(f"  {i}. {v}")
    print("\nSample entry:")
    for k, val in results["sample_entry"].items():
        print(f"  {k}: {val}")
    print(f"\nRow count: {results['row_count']}")

def average_body_mass_by_species_and_island(data):
    """
    Compute average body_mass_g for each species and island combination.
    """
    sums = {}
    counts = {}
    
    for row in data:
        species = row.get("species")
        island = row.get("island")
        mass = row.get("body_mass_g")
        
        if not species or species == "" or not island or island == "":
            continue
        if mass in (None, "", "NA"):
            continue
            
        try:
            mass_val = float(mass)
        except Exception:
            continue
            
        key = (species, island)
        
        sums[key] = sums.get(key, 0.0) + mass_val
        counts[key] = counts.get(key, 0) + 1
    
    results = []
    for (species, island), total in sums.items():
        cnt = counts.get((species, island), 0)
        if cnt > 0:
            results.append({
                "species": species,
                "island": island,
                "average_body_mass_g": round(total / cnt, 2)
            })
    
    return results

def sex_ratio_by_species_and_island(data):
    """
    Compute male/female counts and male proportion per species and island.
    """
    counts_dict = {}
    
    for row in data:
        species = row.get("species")
        island = row.get("island")
        sex = row.get("sex")
            
        key = (species, island)
        if key not in counts_dict:
            counts_dict[key] = {"male_count": 0, "female_count": 0, "unknown_count": 0}
            
        if sex in ("NA"):
            counts_dict[key]["unknown_count"] += 1
            continue
        
        if sex == "male":
            counts_dict[key]["male_count"] += 1
        elif sex == "female":
            counts_dict[key]["female_count"] += 1
        else:
            counts_dict[key]["unknown_count"] += 1
            
    results = []
    for (species, island), counts in counts_dict.items():
        known_total = counts["male_count"] + counts["female_count"]
        if known_total == 0:
            male_proportion = None
        else:
            male_proportion = round(counts["male_count"] / known_total, 3)
            
        results.append({
            "species": species,
            "island": island,
            "male_count": counts["male_count"],
            "female_count": counts["female_count"],
            "unknown_count": counts["unknown_count"],
            "male_proportion": male_proportion
        })
    
    return results

def write_results_to_csv(header, rows, outpath):
    """Write header and rows (list of lists) into CSV file at outpath."""
    with open(outpath, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)

class TestPenguinAnalysis(unittest.TestCase):
    
    def test_average_body_mass_basic(self):
        sample1 = [
            {"species": "Adelie", "island": "Torgersen", "body_mass_g": 3700},
            {"species": "Adelie", "island": "Torgersen", "body_mass_g": 3600},
        ]
        res1 = average_body_mass_by_species_and_island(sample1)
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0]["species"], "Adelie")
        self.assertEqual(res1[0]["island"], "Torgersen")
        self.assertAlmostEqual(res1[0]["average_body_mass_g"], 3650.0, places=2)

    def test_average_body_mass_multiple_islands(self):
        sample2 = [
            {"species": "Adelie", "island": "Torgersen", "body_mass_g": 3700},
            {"species": "Adelie", "island": "Biscoe", "body_mass_g": 3500},
            {"species": "Adelie", "island": "Dream", "body_mass_g": 3600},
        ]
        res2 = average_body_mass_by_species_and_island(sample2)
        self.assertEqual(len(res2), 3)

    def test_average_body_mass_missing_data(self):
        sample3 = [
            {"species": "Gentoo", "island": "Biscoe", "body_mass_g": ""},
            {"species": "Gentoo", "island": "Biscoe", "body_mass_g": 5000},
        ]
        res3 = average_body_mass_by_species_and_island(sample3)
        self.assertEqual(len(res3), 1)
        self.assertEqual(res3[0]["species"], "Gentoo")
        self.assertEqual(res3[0]["island"], "Biscoe")
        self.assertAlmostEqual(res3[0]["average_body_mass_g"], 5000.0, places=2)

    def test_average_body_mass_empty_island(self):
        sample4 = [
            {"species": "Chinstrap", "island": "", "body_mass_g": 3800},
            {"species": "Chinstrap", "island": "Dream", "body_mass_g": 3700},
        ]
        res4 = average_body_mass_by_species_and_island(sample4)
        self.assertEqual(len(res4), 1)
        self.assertEqual(res4[0]["island"], "Dream")

    def test_sex_ratio_mixed_sexes(self):
        sample1 = [
            {"species": "Adelie", "island": "Torgersen", "sex": "male"},
            {"species": "Adelie", "island": "Torgersen", "sex": "female"},
            {"species": "Gentoo", "island": "Biscoe", "sex": "male"},
        ]
        res1 = sex_ratio_by_species_and_island(sample1)
        self.assertEqual(len(res1), 2)
        
        adelie_torg = [r for r in res1 if r["species"] == "Adelie" and r["island"] == "Torgersen"][0]
        self.assertEqual(adelie_torg["male_count"], 1)
        self.assertEqual(adelie_torg["female_count"], 1)
        self.assertAlmostEqual(adelie_torg["male_proportion"], 0.5, places=2)

    def test_sex_ratio_multiple_entries(self):
        sample2 = [
            {"species": "Adelie", "island": "Dream", "sex": "male"},
            {"species": "Adelie", "island": "Dream", "sex": "male"},
            {"species": "Adelie", "island": "Dream", "sex": "female"},
        ]
        res2 = sex_ratio_by_species_and_island(sample2)
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0]["male_count"], 2)
        self.assertEqual(res2[0]["female_count"], 1)
        self.assertAlmostEqual(res2[0]["male_proportion"], 0.667, places=3)

    def test_sex_ratio_unknown_sexes(self):
        sample3 = [
            {"species": "Chinstrap", "island": "Dream", "sex": ""},
            {"species": "Chinstrap", "island": "Dream", "sex": ""},
            {"species": "Chinstrap", "island": "Dream", "sex": "male"},
        ]
        res3 = sex_ratio_by_species_and_island(sample3)
        self.assertEqual(len(res3), 1)
        self.assertEqual(res3[0]["unknown_count"], 2)
        self.assertEqual(res3[0]["male_count"], 1)
        self.assertEqual(res3[0]["male_proportion"], 1.0)

    def test_sex_ratio_empty_island(self):
        sample4 = [
            {"species": "Adelie", "island": "", "sex": "male"},
            {"species": "Adelie", "island": "Torgersen", "sex": "female"},
        ]
        res4 = sex_ratio_by_species_and_island(sample4)
        self.assertEqual(len(res4), 1)
        self.assertEqual(res4[0]["island"], "Torgersen")
        self.assertEqual(res4[0]["female_count"], 1)

def main():
    csv_path = "penguins.csv"
    print("Importing dataset...")
    data = import_csv_data(csv_path)
    if not data:
        print("No data loaded. Please check the CSV file path and format.", file=sys.stderr)
        return

    summary = analyze_dataset(data)
    display_analysis_results(summary)

    print("\nRunning unit tests for analysis functions...")
    unittest.main(exit=False, verbosity=2)

    print("\nComputing average body mass by species and island...")
    avg_mass = average_body_mass_by_species_and_island(data)
    print("Computed averages for species and island combinations:")
    for item in avg_mass:
        print(f"  {item['species']} - {item['island']}: {item['average_body_mass_g']}g")

    print("\nComputing sex ratio by species and island...")
    sex_stats = sex_ratio_by_species_and_island(data)
    print("Computed sex statistics for species and island combinations:")
    for item in sex_stats:
        print(f"  {item['species']} - {item['island']}: male={item['male_count']}, female={item['female_count']}, male_prop={item['male_proportion']}")

    avg_rows = [["species", "island", "average_body_mass_g"]]
    for item in avg_mass:
        avg_rows.append([item["species"], item["island"], item["average_body_mass_g"]])
    write_results_to_csv(avg_rows[0], avg_rows[1:], "avg_mass.csv")
    print("\nSaved average body mass by species and island to avg_mass.csv")

    sex_header = ["species", "island", "male_count", "female_count", "unknown_count", "male_proportion"]
    sex_rows = []
    for item in sex_stats:
        mp = "" if item["male_proportion"] is None else item["male_proportion"]
        sex_rows.append([item["species"], item["island"], item["male_count"], item["female_count"], item["unknown_count"], mp])
    write_results_to_csv(sex_header, sex_rows, "sex_ratio.csv")
    print("Saved sex ratio by species and island to sex_ratio.csv")

    print("\nAll done. Please check avg_mass.csv and sex_ratio.csv.")

if __name__ == "__main__":
    main()