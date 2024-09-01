# Data Blender

Data Blender is a web-based tool that allows users to easily combine multiple Excel files, focusing on a specific tab across all files. This tool is designed to streamline data consolidation processes, making it ideal for data analysts, researchers, and anyone working with multiple spreadsheets.

![Data Blender Demo](path/to/demo.gif)

![Data Blender](datablender.png)



## Features

- Drag-and-drop interface for easy file upload
- Support for multiple file formats (.xlsx, .xls, .csv, .tsv, .xml)
- Ability to select a specific tab for combination across all files
- Real-time progress tracking
- Automatic combination of selected files
- List of recently combined files for easy access

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- Pandas
- OpenPyXL

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/data-blender.git
   ```

2. Navigate to the project directory:
   ```
   cd data-blender
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Start the server:
   ```
   uvicorn main:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

1. Drag and drop your Excel files into the upload area, or click "Choose files" to select them.
2. Once files are uploaded, select the tab you want to combine from the options that appear.
3. Click the "Combine Files" button to merge your selected files and tabs.
4. Wait for the process to complete. The progress bar will show the current status.
5. Once complete, your combined file will appear in the "Recent Combined Files" section.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Tailwind CSS](https://tailwindcss.com/) for styling

## Contact

Wilson - [@yourtwitter](https://twitter.com/wilsonusmanjr) - email@example.com

Project Link: [https://github.com/wilsonusman/data-blender](https://github.com/wilsonusman/data-blender)