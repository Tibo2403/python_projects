import zipfile
import shutil

fichier_zip = zipfile.ZipFile("fichiers_excel.zip", 'w')
fichier_zip.write("octobre.xlsx")
fichier_zip.write("novembre.xlsx")
fichier_zip.write("decembre.xlsx")
fichier_zip.close()

# shutil.make_archive("fichiers_excel2","zip","fichiers_excel2")

shutil.unpack_archive("fichiers_excel2.zip","extraction_zip")