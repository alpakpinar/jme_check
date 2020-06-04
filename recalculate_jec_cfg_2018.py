import FWCore.ParameterSet.Config as cms

# Define the CMSSW process
process = cms.Process("RERUN")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet( 
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False) 
)

# How many events to process
process.maxEvents = cms.untracked.PSet( 
   input = cms.untracked.int32(5000)
)

#configurable options =======================================================================
usePrivateSQlite=False #use external JECs (sqlite file)
#===================================================================


### External JECs =====================================================================================================

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20' # for 2018 samples

### =====================================================================================================
fnames = [
    '/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/00000/BA9E480E-209A-494A-8936-27484D4BA86A.root'
]

# Define the input source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(fnames)
)

# --------------------------
# Jet correction
# --------------------------
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJets'),
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')  # Update: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
)

process.jecSequence = cms.Sequence(process.patJetCorrFactors * process.updatedPatJets)

# --------------------------
# MET correction: Also apply EEfix 2017 if running over 2017 sample
# --------------------------
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

runMetCorAndUncFromMiniAOD(process,
                        isData=False,
                        )

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = cms.untracked.vstring( "keep *_slimmedMETs_*_*",
                                            "keep *_slimmedMETsNoHF_*_*",
                                            "keep *_slimmedJets_*_*",
                                            "keep *_slimmedMuons_*_*",
                                            "keep *_slimmedElectrons_*_*",
                                            "keep *_offlineSlimmedPrimaryVertices_*_*",
                                            "keep *_updatedPatJets_*_*",
                                            "keep *_basicJetsForMet_*_*",
                                            "keep *_cleanedPatJets_*_*",
                                            "keep *_shiftedPatJetEnDown_*_*",
                                            "keep *_shiftedPatJetEnUp_*_*",
                                            "keep *_shiftedPatJetResDown_*_*",
                                            "keep *_shiftedPatJetResUp_*_*",
                                            "keep *_patSmearedJets_*_*",
                                            "keep *_patPFMet_*_*",
                                            "keep *_patPFMetT1_*_*",
                                            "keep *_patPFMetT1Smear_*_*",
                                            "keep *_patPFMetT1JetResDown_*_*",
                                            "keep *_patPFMetT1JetResUp_*_*",
                                            "keep *_patPFMetT1JetEnDown_*_*",
                                            "keep *_patPFMetT1JetEnUp_*_*",
                                            "keep *_patPFMetT1Smear_*_*",
                                            "keep *_patPFMetT1SmearJetResDown_*_*",
                                            "keep *_patPFMetT1SmearJetResUp_*_*",
                                            "keep *_patPFMetT1Puppi_*_*",
                                            "keep *_slimmedMETsPuppi_*_*",
                                            ),
    # fileName = cms.untracked.string('./miniaod/2018/debug_1000events_fixSmearFactor.root'),
    fileName = cms.untracked.string('./miniaod/2018/first_5000_events_fixSmear.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

process.MINIAODSIMoutput_step = cms.EndPath(process.jecSequence * process.fullPatMetSequence * process.MINIAODSIMoutput)
