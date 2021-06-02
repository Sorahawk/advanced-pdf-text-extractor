import glob, os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path, pdfinfo_from_path


mainPath = os.getcwd()
outputPath = mainPath + '\\Output'

os.chdir(mainPath + '\\Input')

for infile in glob.glob('*.pdf'):
	pdfInfo = pdfinfo_from_path(infile)
	maxPages = pdfInfo["Pages"]

	pageCounter = 1
	for pageNum in range(1, maxPages + 1, 10) : 
		pdfPages = convert_from_path(infile, 300, first_page=pageNum, last_page=min(pageNum + 9, maxPages))

		for page in pdfPages:
			pageImageName = '{} p{}.jpg'.format(infile[:-4], pageCounter)
			page.save(pageImageName, 'JPEG')
			pageCounter += 1

	outfileName = "{}\\{}txt".format(outputPath, infile[:-3])
	with open(outfileName, 'w') as outfile:
		for pageNum in range(1, pageCounter):
			pageImageName = '{} p{}.jpg'.format(infile[:-4], pageNum)
			image = Image.open(pageImageName)

			pageText = str(pytesseract.image_to_string(image)).replace('-\n', '')
			outfile.write(pageText)

			os.remove(pageImageName)

	print('Extraction for {} completed.'.format(infile))
print('All files successfully extracted.')
