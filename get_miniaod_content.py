import ROOT
ROOT.gROOT.SetBatch(True)
import pickle

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

# Load in JEC uncertainties
jetunc = ROOT.JetCorrectionUncertainty('Autumn18_V19/Autumn18_V19_MC_Uncertainty_AK4PFchs.txt')

jets, jetLabel = Handle("std::vector<pat::Jet>"), "updatedPatJets"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
t1CorrectedMets, t1CorrectedMetLabel = Handle("std::vector<pat::MET>"), "patPFMetT1"
smearedMets, smearedMetLabel = Handle("std::vector<pat::MET>"), "patPFMetT1Smear"
smearedMets_jerDown, smearedMetLabel_jerDown = Handle("std::vector<pat::MET>"), "patPFMetT1SmearJetResDown"
smearedMets_jerUp, smearedMetLabel_jerUp = Handle("std::vector<pat::MET>"), "patPFMetT1SmearJetResUp"
cleaned_jets_, cleaned_jets_label = Handle("std::vector<pat::Jet>"), "cleanedPatJets"
jets_for_met_, jets_for_met_label = Handle("std::vector<pat::Jet>"), "basicJetsForMet"
jets_shiftUp_, jets_shiftUp_label = Handle("std::vector<pat::Jet>"), "shiftedPatJetEnUp"
jets_shiftDown_, jets_shiftDown_label = Handle("std::vector<pat::Jet>"), "shiftedPatJetEnDown"
smearedJets_, smearedJetLabel = Handle("std::vector<pat::Jet>"), "patSmearedJets"
jets_jerUp, jets_jerUp_label = Handle("std::vector<pat::Jet>"), "shiftedPatJetResUp"
jets_jerDown, jets_jerDown_label = Handle("std::vector<pat::Jet>"), "shiftedPatJetResDown"
# jets_forT1Smear_, jets_forT1Smear_label = Handle("std::vector<pat::Jet>"), "selectedPatJetsForMetT1T2SmearCorr" 

# protocol = 'root://cmsxrootd.fnal.gov/'
# input_file = protocol + '/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/3C778035-7343-E811-A9AA-484D7E8DF0B9.root'
# input_file = protocol + '/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/AC04E4FB-D243-E811-87DA-0242AC1C0501.root'
# input_file = protocol + '/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/00000/E77C132D-17C8-EF46-BBC2-E1434D0564C4.root'
#input_file = './miniaod/miniaod_with_leptons_5000.root'
# input_file = './miniaod/2018/first_5000_events_smearfix.root'
input_file = './debug2018_var1.root'

events = Events(input_file)

for iev,event in enumerate(events):
    if iev == 10: break
    event.getByLabel(jetLabel, "", "RERUN", jets)
    event.getByLabel(metLabel, "", "RERUN", mets)
    event.getByLabel(t1CorrectedMetLabel, "", "RERUN", t1CorrectedMets)
    event.getByLabel(smearedMetLabel, "", "RERUN", smearedMets)
    event.getByLabel(smearedMetLabel_jerUp, "", "RERUN", smearedMets_jerUp)
    event.getByLabel(smearedMetLabel_jerDown, "", "RERUN", smearedMets_jerDown)
    event.getByLabel(jets_jerUp_label, "", "RERUN", jets_jerUp)
    event.getByLabel(jets_jerDown_label, "", "RERUN", jets_jerDown)
    event.getByLabel(cleaned_jets_label, "", "RERUN", cleaned_jets_)
    event.getByLabel(jets_for_met_label, "", "RERUN", jets_for_met_)
    event.getByLabel(jets_shiftUp_label, "", "RERUN", jets_shiftUp_)
    event.getByLabel(jets_shiftDown_label, "", "RERUN", jets_shiftDown_)
    event.getByLabel(smearedJetLabel, "", "RERUN", smearedJets_)
    # event.getByLabel(jets_forT1Smear_label, "", "RERUN", jets_forT1Smear_)

    # Print event information
    run = event.eventAuxiliary().run()
    lumi = event.eventAuxiliary().luminosityBlock()
    event = event.eventAuxiliary().event()
    # if event != 10851233:
        # continue
    #if not (lumi in [62006, 9137, 23111, 59523, 28599, 64660, 49747, 77921, 27483, 48876, 48924, 49499, 49873, 45412, 13301, 14293, 4242] and event in [9136468, 62004266, 23110153, 59522846, 28598888, 64659022, 49746759, 77920800, 27482094, 48875897, 48923775, 49498678, 49872332, 45411773, 13300422, 14292908, 4241946]):
     #   continue
    # if not (lumi in [4323, 57382, 57072, 32983, 57324, 58893, 21912, 22142, 62098, 60344, 60340, 62664] and event in [4322295, 57381240, 57071805, 32982715, 57323947, 58892265, 21911415, 22141683, 62097097, 60343717, 60339783, 62663643]):
        # continue
    print('*'*20)
    print('Run: %2d, Lumi: %4d, Event: %8d' % (run, lumi, event))
    ak4 = jets.product()
    jets_for_met = jets_for_met_.product()
    cleaned_jets = cleaned_jets_.product()
    jets_shiftUp = jets_shiftUp_.product()
    jets_shiftDown = jets_shiftDown_.product()
    smearedJets = smearedJets_.product()
    ak4_jerUp = jets_jerUp.product()
    ak4_jerDown = jets_jerDown.product()
    # ak4_T1smear = jets_forT1Smear_.product()

    num_cleaned_jets = len(cleaned_jets)
    num_jetsShiftUp = len(jets_shiftUp)
    num_jetsShiftDown = len(jets_shiftDown)
    num_jets_for_met = len(jets_for_met)
    num_jets = len(ak4)
    num_smeared_jets = len(smearedJets)

    # num_jets_jerUp = len(ak4_jerUp)
    # num_jets_jerDown = len(ak4_jerDown)
    # print('Number of jets in JER up coll: %d' % num_jets_jerUp)
    # print('Number of jets in JER down coll: %d' % num_jets_jerDown)

#    print('-'*20)
#    print('SMEARED JETS')
#    print('-'*20)
#    for i,j in enumerate(smearedJets):
#        jet_pt = j.pt()
#        jet_px = j.px()
#        jet_py = j.py()
#        jet_eta = j.eta()
#        # print('Jet pt: %.3f' % jet_pt)
#        print('Smeared jet px: %.3f' % jet_px)
#        print('Smeared jet py: %.3f' % jet_py)
#        # print('Jet eta: %.3f' % jet_eta)
#        j_up = ak4_jerUp[i]
#        j_down = ak4_jerDown[i]
#        print('Jet px JER up: %.3f' % j_up.px())
#        print('Jet py JER up: %.3f' % j_up.py())
#        print('Jet px JER down: %.3f' % j_down.px())
#        print('Jet py JER down: %.3f' % j_down.py())
#
#    print('-'*20)
#    print('JETS FOR T1+SMEAR MET calculation')
#    print('-'*20)

    # for i, j in enumerate(ak4_T1smear):
        # jet_pt = j.pt()
        # jet_px = j.px()
        # jet_py = j.py()
        # jet_eta = j.eta()
        # print('*'*20)
        # print('Jet px: %.3f' % jet_px)
        # print('Jet py: %.3f' % jet_py)

    # for i, j in enumerate(cleaned_jets):
        # # Get nominal jet pt and eta
        # jet_pt = j.pt()
        # jet_eta = j.eta()
        # # Get JES up/down jet pt for each jet
        # jet_pt_jesUp = jets_shiftUp[i].pt()
        # jet_pt_jesDown = jets_shiftDown[i].pt()
        # cleaned_jets_pt = cleaned_jets[i].pt()
        # jet_pt_l1 = cleaned_jets_pt * j.jecFactor('L1FastJet')
        # # print('Jet pt in slimmedJets collection: %.3f' % jet_pt)
        # # print('Jet eta in slimmedJets collection: %.3f' % jet_eta)
        # print('-'*20)
        # print('L1 corrected jet pt: %.3f' % jet_pt_l1)
        # print('L1L2L3 corrected jet pt: %.3f' % cleaned_jets_pt)
        # print('Jet pt JES up: %.3f' % jet_pt_jesUp)
        # print('Jet pt JES down: %.3f' % jet_pt_jesDown)

        # --------------------------
        # NOTE: Do not use this portion
        # --------------------------
        # jetunc.setJetPt(jet_pt)
        # jetunc.setJetEta(jet_eta)
        # unc = jetunc.getUncertainty(True)
        # jet_pt_l1 = jet_pt * j.jecFactor('L1FastJet')
        # print('*'*20)
        # print('Uncertainty: %.5f' % unc)
        # print('Jet pt fed in: %.5f' % jet_pt)
        # print('Jet eta fed in: %.5f' % jet_eta)
        # #print('Jet px: %.5f' % j.px())
        # #print('Jet py: %.5f' % j.py())
        # print('L1 corrected jet pt: %.5f' % jet_pt_l1)
        # jet_pt_jesup = jet_pt*(1+unc)
        # jet_pt_jesdown = jet_pt*(1-unc)
        # print('Jet pt: %.3f, Jet pt JES up: %.3f, Jet pt JES down: %.3f, Jet eta: %.3f' % (jet_pt, jet_pt_jesup, jet_pt_jesdown, jet_eta))
        # print('Jet eta: %.3f' % jet_eta)
        # raw_factor = j.jecFactor('Uncorrected')
        # raw_jet_pt = jet_pt * raw_factor
        # print('Raw jet pt: %.3f' % raw_jet_pt)
        # --------------------------

    met = mets.product().front()
    # Smeared and T1 corrected MET pt
    met_pt_jer = met.corPt(6) # Type1Smear
    calo_met_pt = met.caloMETPt()
    raw_met_pt = met.corPt(0)
    smeared_met = smearedMets.product().front()
    t1_met = t1CorrectedMets.product().front()
    # print('Calo MET pt: %.3f' % calo_met_pt)
    # print('Raw MET pt: %.3f' % raw_met_pt)
    print('T1 corrected MET pt: %.3f' % met.pt())
    print('Smeared + T1 corrected MET pt: %.3f' % met_pt_jer)
    # print('Smeared + T1 corrected MET pt from slimmedMETs coll: %.3f' % met_pt_jer)
    # print('T1 corrected MET pt from slimmedMETs coll: %.3f' % met.pt())
    # print('T1 corrected MET pt from patPFMetT1 coll: %.3f' % t1_met.pt())
    
    met_pt_jerUp = met.shiftedPt(0, 6) # MET corr level: Type1Smear
    met_pt_jerDown = met.shiftedPt(1, 6) # MET corr level: Type1Smear

    smeared_met_jerUp = smearedMets_jerUp.product().front()
    smeared_met_jerDown = smearedMets_jerDown.product().front()
    
    met_pt_jerUp_smeared = smeared_met_jerUp.pt()
    met_pt_jerDown_smeared = smeared_met_jerDown.pt()

    print('MET pt JER up from slimmedMETs collection: %.3f' % met.shiftedPt(0))
    print('MET pt JER up from slimmedMETs collection Type1Smear: %.3f' % met_pt_jerUp)
    print('MET pt JER up from patPFMetT1SmearJetResUp collection: %.3f' % met_pt_jerUp_smeared)
    print('MET pt JER down from slimmedMETs collection: %.3f' % met.shiftedPt(1))
    print('MET pt JER down from slimmedMETs collection Type1Smear: %.3f' % met_pt_jerDown)
    print('MET pt JER down from patPFMetT1SmearJetResDown collection: %.3f' % met_pt_jerDown_smeared)
