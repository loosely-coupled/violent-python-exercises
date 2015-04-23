import pyPdf
import optparse
from pyPdf import PdfFileReader

def printMeta(filename):

	pdfFile = PdfFileReader(file(filename, 'rb'))
	docInfo = pdfFile.getDocumentInfo()

	print '[+] PDF MetaData for : ' + str(filename)
	for metaItem in docInfo:
		print '[+]' + metaItem + ":" + docInfo[metaItem]

def main():

	parser = optparse.OptionParser('usage %prog -F <PDF file name>')
	parser.add_option('-F', dest='filename', type='string', help='specify file name')

	(option, args) = parser.parse_args()

	filename = option.filename

	if filename == None:
		print parser.usage
		exit(0)

	else:
		printMeta(filename)

if __name__ == "__main__":
	main()