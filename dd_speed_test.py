#!/usr/bin/python

import sys, getopt
from subprocess import PIPE, Popen
import resource

def dd_test(inputfile='/dev/zero', outputfile='disk_file', logfile='log.txt', sizef=64, iteration=5, device=False):
	print (f'Входной файл "{inputfile}"')
	print (f'Выходной файл "{outputfile}"')
	print (f'Лог файл "{logfile}"')
	print (f'Размер файла {sizef} MiB')
	print (f'Количество итераций {iteration}')
	print (f'Аппаратный диск? = {device}')

	bs_s = [
	"s",
	"1K",
	"2K",
	"4K",
	"8K",
	"16K",
	"32K",
	"64K",
	"128K",
	"256K",
	"512K",
	"1M",
	"2M",
	"4M",
	"8M",
	"16M"]

	bs_bytes = [
	512,
	1024,
	2048,
	4096,
	8192,
	16384,
	32768,
	65536,
	131072,
	262144,
	524288,
	1048576,
	2097152,
	4194304,
	8388608,
	16777216
	]
	
	testfilesize = sizef * 1024 * 1024
	dd_str = ''
	with open(logfile, 'w') as filelog:
		filelog.write("#bs\ttime_write_average\ttime_med\ttime_write0\ttime_write1\ttime_write2\n")
		bs_pos = 0
		for bs in bs_bytes:
			result_time = []
			for i in range(iteration):
				if device:
					dd_str = f'bash -c "time sh -c \\"dd if={inputfile} of={outputfile} bs={bs} count={testfilesize//bs} seek={testfilesize * bs_pos} conv=fdatasync && sync\\""'
				else:
					dd_str = f'bash -c "time sh -c \\"dd if={inputfile} of={outputfile} bs={bs} count={testfilesize//bs} conv=fdatasync && sync\\""'
				print(dd_str)
				p = Popen(dd_str, shell=True, stdin=PIPE, stderr=PIPE)
				stderr = p.communicate()[1].decode('utf-8')
				print(f"stderr = {stderr}")
				for str in stderr.split("\n"):
					if "real" in str.split("\t")[0]:
						real = str.split("\t")[1]
						result_time.append(float(real.split("m")[0])*60 + float(real.split("m")[1][:-1]))
						break
			print(f"result_time = {result_time}")
			result_time.sort()
			result_aver = 0 
			for i in range(iteration):
				result_aver += result_time[i]
			filelog.write(f"{bs_s[bs_pos]}\t{round( result_aver / iteration, 3)}\t{result_time[iteration // 2]}\t{result_time[0]}\t{result_time[1]}\t{result_time[2]}\t{bs}\n")
			bs_pos += 1


def help():
	print ('Use:\ndd_speed_test.py -i <filename to read> -o <filename to write> -l <filename log> -s <size MiB> -n <iteration> -d')
	print('or:\ndd_speed_test.py --ifile=<filename> --ofile=<filename> --logfile=<filename log> --size=<size MiB> --iteration=<iteration>')
	print('default input file "/dev/zero/" output file "disk_file" logfile "log.txt" size=64 iteration=5')
	print('example: dd_speed_test.py -i /dev/zero -o /dev/null -l no.txt -s 256 -n 9')

def main(argv):
	inputfile = '/dev/zero'
	outputfile = 'disk_file'
	logfile = 'log.txt'
	sizef = 64
	iteration = 5
	device = False
	try:
		opts, args = getopt.getopt(argv,"hi:o:i:s:n:d",["ifile=","ofile=","logfile=","size=","iteration="])
	except getopt.GetoptError:
		help()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			help()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-l", "--logfile"):
			logfile = arg
		elif opt in ("-s", "--size"):
			if arg.isnumeric():
				sizef=int(arg)
			else:
				print('Size error!')
				help()
				sys.exit(2)
		elif opt in ("-n", "--iteration"):
			if arg.isnumeric():
				iteration=int(arg)
			else:
				print('Iteration error!')
				help()
				sys.exit(2)
		elif opt in ("-d"):
			device=True

	dd_test(inputfile, outputfile, logfile, sizef, iteration, device)

if __name__ == "__main__":
	main(sys.argv[1:])
