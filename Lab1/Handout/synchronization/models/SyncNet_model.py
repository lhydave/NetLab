import torch
import torch.nn as nn
from .base_model import BaseModel
from . import networks
import os


class SyncNetModel(BaseModel):
    """
    This class implements the SyncNet model, for learning synchronization between video and audio with paired data.

    The model training requires 'NoImplemented' dataset.
    By default, it uses a

    SyncNet paper:
    """

    @staticmethod
    def modify_commandline_options(parser, is_train=True):
        """Add new dataset-specific options, and rewrite default values for existing options.
        Parameters:
            parser          -- original option parser
            is_train (bool) -- whether training phase or test phase. You can use this flag to add training-specific or test-specific options.
        Returns:
            the modified parser.
        For SyncNet, no addition
        """
        # Load models from pth file
        parser.add_argument('--load_specific_model', action='store_true', help='load a existing model specified by user')
        parser.add_argument('--model_load_path', type=str, default='', help='path of trained models')
        parser.add_argument('--video_model_file', type=str, default='', help='name of trained video model')
        parser.add_argument('--audio_model_file', type=str, default='', help='name of trained audio model')

        return parser

    def __init__(self, opt):
        """Initialize the SyncNet class.
        Parameters:
            opt (Option class)-- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseModel.__init__(self, opt)
        # specify the training losses you want to print out. The training/test scripts will call <BaseModel.get_current_losses>
        self.loss_names = ['ContrastiveLoss']

        # specify the models you want to save to the disk. The training/test scripts will call <BaseModel.save_networks> and <BaseModel.load_networks>.
        self.model_names = ['_Video', '_Audio']

        # define networks
        self.net_Video = networks.define_V('SyncNet', opt.norm, opt.init_type, opt.init_gain, self.gpu_ids)
        self.net_Audio = networks.define_A('SyncNet', opt.norm, opt.init_type, opt.init_gain, self.gpu_ids)

        if self.isTrain:
            # define loss functions
            self.criterion = networks.ContrastiveLoss().to(self.device)  # define ContrastiveLoss.

            # initialize optimizers; schedulers will be automatically created by function <BaseModel.setup>.
            self.optimizer_V = torch.optim.Adam(self.net_Video.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
            self.optimizer_A = torch.optim.Adam(self.net_Audio.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
            self.optimizers.append(self.optimizer_V)
            self.optimizers.append(self.optimizer_A)

    def set_input(self, input):
        """
            No Implemented
        """
        self.vinput = input['vfeat'].to(self.device)
        self.ainput = input['afeat'].to(self.device)
        self.label = input['label'].to(self.device)

    def forward(self):
        """Run forward pass; called by both functions <optimize_parameters> and <test>."""
        self.vfeat = self.net_Video(self.vinput)
        self.afeat = self.net_Audio(self.ainput)

    def backward(self):
        """Calculate ContrastiveLoss """
        self.loss = self.criterion(self.vfeat, self.afeat, self.label, self.device)
        self.loss.backward()

    def optimize_parameters(self):
        self.forward()
        self.optimizer_A.zero_grad()
        self.optimizer_V.zero_grad()

        self.backward()
        self.optimizer_V.step()
        self.optimizer_A.step()

    def get_current_losses(self):
        return self.loss

    def get_features_and_label(self):
        return self.vfeat, self.afeat, self.label

    def setup(self, opt):
        """Load and print networks; create schedulers
        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        if self.isTrain:
            self.schedulers = [networks.get_scheduler(optimizer, opt) for optimizer in self.optimizers]
        if not self.isTrain or opt.continue_train:
            if opt.load_specific_model:
                video_model_file = os.path.join(opt.model_load_path, opt.video_model_file)
                print('loading the video net from %s' % video_model_file)
                net_Video_state_dict = torch.load(video_model_file, map_location=str(self.device))
                self.net_Video.module.load_state_dict(net_Video_state_dict)

                audio_model_file = os.path.join(opt.model_load_path, opt.audio_model_file)
                print('loading the audio net from %s' % audio_model_file)
                net_Audio_state_dict = torch.load(audio_model_file, map_location=str(self.device))
                self.net_Audio.module.load_state_dict(net_Audio_state_dict)
                print("load specific model successfully.")
            else:
                load_suffix = 'iter_%d' % opt.load_iter if opt.load_iter > 0 else opt.epoch
                self.load_networks(load_suffix)
        self.print_networks(opt.verbose)



