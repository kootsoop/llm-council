from ari import store_in_pickle, load_from_pickle
import os
import argparse
import asyncio
from markdown_pdf import Section
from markdown_pdf import MarkdownPdf
from council import run_full_council, generate_conversation_title, stage1_collect_responses, stage2_collect_rankings, stage3_synthesize_final, calculate_aggregate_rankings  # noqa: F401


async def run_command_line_query(file_name):
	"""
	Run a command line query against the LLM Council.
	"""
	with open("egr1110_grading_prompt.txt", "r") as f:
		query = f.read()

	with open(file_name, "r") as f:
		query = query + "\n" + f.read()

	print(f"Running LLM Council for query: {query}")
	final_response = await run_full_council(query)  # noqa: F704
	return final_response


def generate_pdf_report(final_response, output_file="llm_council_report.pdf"):
	"""
	Generate a PDF report from the final response.
	"""
	pdf = MarkdownPdf(toc_level=2, optimize=True)
	pdf.add_section(Section(final_response[2]['response']))
	pdf.meta["title"] = "First cut at report"
	pdf.meta["author"] = "LLM Council (by Andrej Karpathy, modified by PJK)"
	pdf.save(output_file)


if __name__ == "__main__":

	# if os.path.exists("final_response.pkl"):
	# 	final_response = load_from_pickle("final_response.pkl")
	# else:
	parser = argparse.ArgumentParser(
		description="Run command line queries against the LLM Council."
	)
	parser.add_argument(
		"query_file",
		type=str,
		help="The query to send to the LLM Council."
	)
	args = parser.parse_args()

	final_response = asyncio.run(run_command_line_query(args.query_file))  # noqa: F704

	print("Final Response from LLM Council:")
	print(final_response)

	# if final_response:
	# 	if not os.path.exists("final_response.pkl"):
	# 		store_in_pickle("final_response.pkl", final_response)

	generate_pdf_report(final_response, output_file=f"{args.query_file}.pdf")