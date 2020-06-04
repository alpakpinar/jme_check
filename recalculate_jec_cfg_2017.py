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
   input = cms.untracked.int32(10)
)

#configurable options =======================================================================
usePrivateSQlite=False #use external JECs (sqlite file)
#===================================================================


### External JECs =====================================================================================================

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = '94X_mc2017_realistic_v17'  

### =====================================================================================================

fnames = [
    '/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/DE549331-1144-E811-984B-44A842CFD667.root'
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

# Parameters for EE2017 fix, if not running over 2017, do not provide those to the function
fixEE2017Params = {'userawPt': True, 'ptThreshold':50.0, 'minEtaThreshold':2.65, 'maxEtaThreshold': 3.139}

runMetCorAndUncFromMiniAOD(process,
                        isData=False,
                        fixEE2017=True,
                        fixEE2017Params=fixEE2017Params
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
                                            "keep *_selectedPatJetsForMetT1T2SmearCorr_*_*",
                                            "keep *_shiftedPatJetEnDown_*_*",
                                            "keep *_shiftedPatJetEnUp_*_*",
                                            "keep *_shiftedPatJetResDown_*_*",
                                            "keep *_shiftedPatJetResUp_*_*",
                                            "keep *_patSmearedJets_*_*",
                                            "keep *_patPFMet_*_*",
                                            "keep *_patPFMetT1_*_*",
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
    fileName = cms.untracked.string('./debug2017.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

process.MINIAODSIMoutput_step = cms.EndPath(process.jecSequence * process.fullPatMetSequence * process.MINIAODSIMoutput)
