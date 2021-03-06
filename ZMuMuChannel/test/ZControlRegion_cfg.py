import FWCore.ParameterSet.Config as cms
from OSUT3Analysis.Configuration.processingUtilities import *
import OSUT3Analysis.DBTools.osusub_cfg as osusub
from OSUT3Analysis.Configuration.configurationOptions import *
import math
import os

################################################################################
##### Set up the 'process' object ##############################################
################################################################################

process = cms.Process ('OSUAnalysis')

# how often to print a log message
process.load ('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.source = cms.Source ('PoolSource',
  fileNames = cms.untracked.vstring (
#    'root://cmsxrootd.fnal.gov//store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/80000/4EF9F71C-0057-E611-A3FF-002590A831AA.root'
#    'root://cmsxrootd.fnal.gov//store/mc/RunIISpring16MiniAODv2/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4/00000/7AADCC01-EC2B-E611-886E-02163E013F02.root'
#    'root://cms-xrd-global.cern.ch//store/data/Run2015D/MuonEG/MINIAOD/16Dec2015-v1/60000/66DF7966-6AAB-E511-BE9D-002590747E40.root'
     'file:/store/user/bcardwell/MuMuSkim_17_02_03/DYJetsToLL_50/MuMuSkim/skim_0.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_1.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_2.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_3.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_4.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_5.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_6.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_7.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_8.root',
    # 'file:/store/user/lantonel/EMuSkim_23Sep/MuonEG_2016D_23Sep/EMuSkimSelection/skim_9.root'

  )
)

# output histogram file name when running interactively
process.TFileService = cms.Service ('TFileService',
    fileName = cms.string ('hist.root')
)

# suppress gen-matching erros
process.load ('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.categories.append ("osu_GenMatchable")
process.MessageLogger.cerr.osu_GenMatchable = cms.untracked.PSet(
    limit = cms.untracked.int32 (0)
)

# number of events to process when running interactively
process.maxEvents = cms.untracked.PSet (
    input = cms.untracked.int32 (-1)
)

data_global_tag = '80X_dataRun2_2016SeptRepro_v3'
mc_global_tag = '80X_mcRun2_asymptotic_2016_miniAODv2_v1'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, mc_global_tag, '')
if osusub.batchMode and (osusub.datasetLabel in types) and (types[osusub.datasetLabel] == "data"):
    print "using global tag " + data_global_tag + "..."
    process.GlobalTag = GlobalTag(process.GlobalTag, data_global_tag, '')
else:
    print "using global tag " + mc_global_tag + "..."


################################################################################
##### Set up the 'collections' map #############################################
################################################################################

# this PSet specifies which collections to get from the input files
miniAOD_collections = cms.PSet (
  electrons       =  cms.InputTag  ('slimmedElectrons',''),
  genjets         =  cms.InputTag  ('slimmedGenJets',                 ''),
  jets            =  cms.InputTag  ('slimmedJets',                    ''),
  bjets           =  cms.InputTag  ('slimmedJets',                    ''),
  generatorweights=  cms.InputTag  ('generator', ''), 
  mcparticles     =  cms.InputTag  ('packedGenParticles',             ''),
  hardInteractionMcparticles  =  cms.InputTag  ('prunedGenParticles',             ''),
  mets            =  cms.InputTag  ('slimmedMETs',                    ''),
  muons           =  cms.InputTag  ('slimmedMuons',                   ''),
  photons         =  cms.InputTag  ('slimmedPhotons',                 ''),
  primaryvertexs  =  cms.InputTag  ('offlineSlimmedPrimaryVertices',  ''),
  pileupinfos     =  cms.InputTag  ('slimmedAddPileupInfo',  ''),
  beamspots       =  cms.InputTag  ('offlineBeamSpot',                ''),
  superclusters   =  cms.InputTag  ('reducedEgamma',                  'reducedSuperClusters'),
  taus            =  cms.InputTag  ('slimmedTaus',                    ''),
  triggers        =  cms.InputTag  ('TriggerResults',                 '',  'HLT'),
  trigobjs        =  cms.InputTag  ('selectedPatTrigger',             ''),
)

collections = miniAOD_collections

################################################################################
##### Set up any user-defined variable producers ###############################
################################################################################

variableProducers = []
weights = cms.VPSet ()
scalingfactorproducers = []

################################################################################
##### Import the channels to be run ############################################
################################################################################

from OSUDisplacedHiggs.ZMuMuChannel.ZControlRegionSelection import *

eventSelections = [ZControlRegion]

################################################################################
##### Import the histograms to be plotted ######################################
################################################################################

from OSUT3Analysis.Configuration.histogramDefinitions import MuonHistograms, DiMuonHistograms 
from OSUDisplacedHiggs.Configuration.histogramDefinitions import MuonD0Histograms#, BeamspotHistograms
from OSUT3Analysis.Configuration.histogramDefinitions import JetHistograms, MuonJetHistograms
from OSUT3Analysis.Configuration.histogramDefinitions import MetHistograms, MuonMetHistograms
from OSUDisplacedHiggs.Configuration.histogramDefinitions import jetHistograms

################################################################################
##### Attach the channels and histograms to the process ########################
################################################################################

histograms = cms.VPSet()
histograms.append(MuonHistograms)
histograms.append(DiMuonHistograms)
histograms.append(MuonD0Histograms)
#histograms.append(BeamspotHistograms)
histograms.append(JetHistograms)
histograms.append(MuonJetHistograms)
histograms.append(MetHistograms)
histograms.append(MuonMetHistograms)
#histograms.append(eventHistograms)
histograms.append(jetHistograms)

add_channels (process, eventSelections, histograms, weights, scalingfactorproducers, collections, variableProducers, True)
