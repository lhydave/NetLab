#!/usr/bin/python
#-*- coding: utf-8 -*-

import time, pdb, argparse, subprocess, pickle, os, gzip, glob, torch, gc

from SyncNetInstance import *

# ==================== PARSE ARGUMENT ====================

parser = argparse.ArgumentParser(description = "SyncNet");
parser.add_argument('--initial_model', type=str, default="data/syncnet_v2.model", help='');
parser.add_argument('--batch_size', type=int, default='20', help='');
parser.add_argument('--vshift', type=int, default='60', help='');
parser.add_argument('--data_dir', type=str, default='data/work', help='');
parser.add_argument('--videofile', type=str, default='', help='');
parser.add_argument('--reference', type=str, default='', help='');
opt = parser.parse_args();

setattr(opt,'avi_dir',os.path.join(opt.data_dir,'pyavi'))
setattr(opt,'tmp_dir',os.path.join(opt.data_dir,'pytmp'))
setattr(opt,'work_dir',os.path.join(opt.data_dir,'pywork'))
setattr(opt,'crop_dir',os.path.join(opt.data_dir,'pycrop'))
gc.collect()
torch.cuda.empty_cache()

# ==================== LOAD MODEL AND FILE LIST ====================

s = SyncNetInstance();

s.loadParameters(opt.initial_model);
print("Model %s loaded."%opt.initial_model);

flist = glob.glob(os.path.join(opt.crop_dir,opt.reference,'0*.avi'))
flist.sort()

# ==================== GET OFFSETS ====================

dists = []
offsets = []
k = 0
w = open('./'+opt.reference+'_offset.txt','w')
with torch.no_grad():
    for idx, fname in enumerate(flist):
        offset, conf, dist = s.evaluate(opt,videofile=fname, num = k)
        k+=1
        print(k)
        dists.append(dist)
        tot_off = 0
        if len(offset) < 100:
            for i in range(len(offset)):
                tot_off += offset[i]
            tot_off /= len(offset)
            w.write(str(tot_off)+'s\n')
        else:
            for i in range(len(offset)):
                if (i+1) % 100 == 0:
                    tot_off += offset[i]
                    tot_off /= 100
                    w.write(str(tot_off)+'s\n')
                    tot_off = 0
                elif i == (len(offset)-1):
                    tot_off += offset[i]
                    tot_off /= (i+1)%100
                    w.write(str(tot_off) + 's\n')

        offsets.append(offset)

      
# ==================== PRINT RESULTS TO FILE ====================

with open(os.path.join(opt.work_dir,opt.reference,'activesd.pckl'), 'wb') as fil:
    pickle.dump(dists, fil)

with open(os.path.join(opt.work_dir,opt.reference,'offsets.pckl'), 'wb') as fil:
    pickle.dump(offsets, fil)