import PyPDF2


def split_pdf_by_pages(input_pdf_path, split_pages, output_pdf_path_prefix="split_pdf", delete_original_file=False):
    try:
        with open(input_pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            if not all(1 <= page <= num_pages for page in split_pages):
                raise ValueError("Error: The split page numbers exceed the range of PDF pages.")
            if not all(split_pages[i] < split_pages[i + 1] for i in range(len(split_pages) - 1)) if len(
                    split_pages) > 1 else False:
                raise Exception("Error: The split page numbers are not arranged in ascending order")

            start_page = 0
            for i, split_page in enumerate(split_pages):
                pdf_writer = PyPDF2.PdfWriter()
                output_pdf_path = f"{output_pdf_path_prefix}_part{i + 1}.pdf"

                for page_num in range(start_page, split_page):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)

                with open(output_pdf_path, 'wb') as output_file:
                    pdf_writer.write(output_file)

                start_page = split_page


            if start_page < num_pages:
                pdf_writer = PyPDF2.PdfWriter()
                output_pdf_path = f"{output_pdf_path_prefix}_part{len(split_pages) + 1}.pdf"

                for page_num in range(start_page, num_pages):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)

                with open(output_pdf_path, 'wb') as output_file:
                    pdf_writer.write(output_file)


        if delete_original_file:
            import os
            os.remove(input_pdf_path)

        return True


    except FileNotFoundError:

        raise FileNotFoundError(f"Error: file is not found {input_pdf_path}")

    except PyPDF2.errors.PdfReadError as e:

        raise PyPDF2.errors.PdfReadError(f"Error: The PDF file cannot be read：{e}")

    except Exception as e:

        raise Exception(e)
