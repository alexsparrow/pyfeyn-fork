pions_dict = {
"gp" : "\Pgp", # pion
"gppm" : "\Pgppm", "gpmp" : "\Pgpmp", # charged pion
"gpm" : "\Pgpm", # negative pion
"gpp" : "\Pgpp", # positive pion
"gpz" : "\Pgpz", # neutral pion
"gpa" : "\Pgpa",
"gpii" : "\Pgpii",
## nice names
"pi" : "\Pgp", "pion" : "\Pgp",
"pipm" : "\Pgppm", "pimp" : "\Pgpmp",
"piplus" : "\Pgpp", "pi+" : "\Pgpp",
"piminus" : "\Pgpm", "pi-" : "\Pgpm",
"pizero" : "\Pgpz", "pi0" : "\Pgpz"
}
hepnames_dict = pions_dict.copy()

etamesons_dict = {
"gh" : "\Pgh",
"ghpr" : "\Pghpr",
"cgh" : "\Pcgh",
"gha" : "\Pgha",
"ghb" : "\Pghb",
"ghpri" : "\Pghpri",
"cghi" : "\Pcghi",
## nice names
"eta" : "\Pgh",
"etaprime" : "\Pghpr",
"etac" : "\Pcgh"
}
hepnames_dict.update(etamesons_dict)

omegamesons_dict = {
"go" : "\Pgo",
"goi" : "\Pgoi",
"goa" : "\Pgoa",
"gob" : "\Pgob",
"goiii" : "\Pgoiii",
## nice names
"omega" : "\Pgo"
}
hepnames_dict.update(omegamesons_dict)

rhomesons_dict = {
"gr" : "\Pgr", # resonance removed
"grp" : "\Pgrp",
"grm" : "\Pgrm",
"grpm" : "\Pgrpm", "grmp" : "\Pgrmp",
"grz" : "\Pgrz",
"gri" : "\Pgri", # new
"gra" : "\Pgra",
"grb" : "\Pgrb",
"griii" : "\Pgriii",
## nice names
"rho" : "\Pgr",
"rhoplus" : "\Pgrp", "rho+" : "\Pgrp",
"rhominus" : "\Pgrm", "rho-" : "\Pgrm",
"rhopm" : "\Pgrpm", "rhomp" : "\Pgrmp",
"rhozero" : "\Pgrz", "rho0" : "\Pgrz"
}
hepnames_dict.update(rhomesons_dict)

amesons_dict = {
"aii" : "\Paii",
"ai" : "\Pai",
"az" : "\Paz",
"bgcia" : "\Pbgcia",
"bgciia" : "\Pbgciia",
"bgcii" : "\Pbgcii",
"bgci" : "\Pbgci",
"bgcza" : "\Pbgcza",
"bgcz" : "\Pbgcz",
"bi" : "\Pbi",
"hia" : "\Phia"
}
hepnames_dict.update(amesons_dict)

fmesons_dict = {
"fia" : "\Pfia",
"fib" : "\Pfib",
"fiia" : "\Pfiia",
"fiib" : "\Pfiib",
"fiic" : "\Pfiic",
"fiid" : "\Pfiid",
"fiipr" : "\Pfiipr",
"fii" : "\Pfii",
"fiv" : "\Pfiv",
"fi" : "\Pfi",
"fza" : "\Pfza",
"fzb" : "\Pfzb",
"fz" : "\Pfz"
}
hepnames_dict.update(fmesons_dict)

phimesons_dict = {
"gf" : "\Pgf",
"gfi" : "\Pgfi",
"gfa" : "\Pgfa",
"gfiii" : "\Pgfiii",
## nice names
"phi" : "\Pgf"
}
hepnames_dict.update(phimesons_dict)

psimesons_dict = {
"Jgy" : "\PJgy",
"Jgyi" : "\PJgyi",
"gy" : "\Pgy",
"gyii" : "\Pgyii",
"gya" : "\Pgya",
"gyb" : "\Pgyb",
"gyc" : "\Pgyc",
"gyd" : "\Pgyd",
## nice names
"Jpsi" : "\PJgy",
"JpsiOneS" : "\PJgyi", "Jpsi(1S)": "\PJgyi",
"psi" : "\Pgy",
"psiTwoS" : "\Pgyii", "psi(2S)" : "\Pgyii"
}
hepnames_dict.update(psimesons_dict)

Upsilonmesons_dict = {
"gU" : "\PgU",
"gUi" : "\PgUi",
"gUa" : "\PgUa",
"gUb" : "\PgUb",
"gUc" : "\PgUc",
"gUd" : "\PgUd",
"gUe" : "\PgUe",
## nice names
"Upsilon" : "\PgU",
"UpsilonOneS" : "\PgUi", "Upsilon(1S)" : "\PgUi",
"UpsilonTwoS" : "\PgUa", "Upsilon(2S)" : "\PgUa",
"UpsilonThreeS" : "\PgUb", "Upsilon(3S)" : "\PgUb",
"UpsilonFourS" : "\PgUc", "Upsilon(4S)" : "\PgUc"
}
hepnames_dict.update(Upsilonmesons_dict)

Kaons_dict = {
"K" : "\PK", # kaon
"Kpm" : "\PKpm", "Kmp" : "\PKmp", # charged kaon
"Km" : "\PKm", # negative kaon
"Kp" : "\PKp", # positive kaon
"Kz" : "\PKz", # neutral kaon
"KzL" : "\PKzL", # K-long
"KzS" : "\PKzS", # K-short
"Kst" : "\PKst", # K star
"aK" : "\PaK", # anti-kaon
"aKz" : "\PaKz", # neutral anti-kaon
"Keiii" : "\PKeiii",
"Kgmiii" : "\PKgmiii",
"Kzeiii" : "\PKzeiii",
"Kzgmiii" : "\PKzgmiii",
"Kia" : "\PKia",
"Kii" : "\PKii",
"Ki" : "\PKi",
"Ksti" : "\PKsti",
"Ksta" : "\PKsta",
"Kstb" : "\PKstb",
"Kstiii" : "\PKstiii",
"Kstii" : "\PKstii",
"Kstiv" : "\PKstiv",
"Kstz" : "\PKstz",
## nice names
"Kplus" : "\PKp", "K+" : "\PKp",
"Kminus" : "\PKm", "K-" : "\PKm",
"Kzero" : "\PKz", "K0" : "\PKz",
"Kshort" : "\PKzS", "Ks" : "\PKzS", "KS" : "\PKzS", 
"Klong" : "\PKzL", "Kl" : "\PKzL", "KL" : "\PKzL",
"Kstar" : "\PKst",
"APK" : "\PaKz", "antiK" : "\PaKz",
"APKzero" : "\PaKz", "antiKzero" : "\PaKz",
"APK0" : "\PaKz", "antiK0" : "\PaKz"
}
hepnames_dict.update(Kaons_dict)

Chi_cmesons_dict = {
"cgc" : "\Pcgc",
"cgcii" : "\Pcgcii",
"cgci" : "\Pcgci",
"cgcz" : "\Pcgcz"
}
hepnames_dict.update(Chi_cmesons_dict)

Dmesons_dict = {
"D" : "\PD",
"Dpm" : "\PDpm", "Dmp" : "\PDmp",
"Dz" : "\PDz",
"Dm" : "\PDm",
"Dp" : "\PDp",
"Dst" : "\PDst",
"aD" : "\PaD",
"aDz" : "\PaDz",
"sD" : "\PsD", # new 2005-07-08
"sDm" : "\PsDm",
"sDp" : "\PsDp",
"sDpm" : "\PsDpm",
"sDmp" : "\PsDmp",
"sDst" : "\PsDst",
"sDipm" : "\PsDipm",
"sDimp" : "\PsDimp",
"Diz" : "\PDiz",
"Dstiiz" : "\PDstiiz",
"Dstpm" : "\PDstpm",
"Dstmp" : "\PDstmp",
"Dstz" : "\PDstz",
## nice names
"Dzero" : "\PDz", "D0" : "\PDz",
"Dminus" : "\PDm", "D-" : "\PDm",
"Dplus" : "\PDp", "D+" : "\PDp",
"Dstar" : "\PDst",
"APD" : "\PaD", "antiD" : "\PaD",
"APDzero" : "\PaDz", "antiDzero" : "\PaDz",
"APD0" : "\PaDz", "antiD0" : "\PaDz",
"Ds" : "\PsD",
"Dsminus" : "\PsDm", "Ds-" : "\PsDm",
"Dsplus" : "\PsDp", "Ds+" : "\PsDp",
"Dspm" : "\PsDpm",
"Dsmp" : "\PsDmp",
"Dsstar" : "\PsDst"
}
hepnames_dict.update(Dmesons_dict)

Bmesons_dict = {
"B" : "\PB",
"Bpm" : "\PBpm", "Bmp" : "\PBmp",
"Bp" : "\PBp",
"Bm" : "\PBm",
"Bz" : "\PBz",
"dB" : "\PdB",
"uB" : "\PuB",
"cB" : "\PcB",
"sB" : "\PsB",
"aB" : "\PaB",
"aBz" : "\PaBz",
"adB" : "\PadB",
"auB" : "\PauB",
"acB" : "\PacB",
"asB" : "\PasB",
## nice names
"Bplus" : "\PBp", "B+" : "\PBp",
"Bminus" : "\PBm","B-" : "\PBm",
"Bzero" : "\PBz","B0" : "\PBz",
"Bd" : "\PdB",
"Bu" : "\PuB",
"Bc" : "\PcB",
"Bs" : "\PsB",
"APB" : "\PaB", "antiB" : "\PaB",
"APBzero" : "\PaBz", "antiBzero" : "\PaBz",
"APB0" : "\PaBz", "antiB0" : "\PaBz",
"APBd" : "\PadB", "antiBd" : "\PadB",
"APBu" : "\PauB", "antiBu" : "\PauB",
"APBc" : "\PacB", "antiBc" : "\PacB",
"APBs" : "\PasB", "antiBs" : "\PasB"
}
hepnames_dict.update(Bmesons_dict)

mesons_dict = pions_dict.copy()
mesons_dict.update(etamesons_dict)
mesons_dict.update(omegamesons_dict)
mesons_dict.update(rhomesons_dict)
mesons_dict.update(phimesons_dict)
mesons_dict.update(amesons_dict)
mesons_dict.update(fmesons_dict)
mesons_dict.update(psimesons_dict)
mesons_dict.update(Upsilonmesons_dict)
mesons_dict.update(Kaons_dict)
mesons_dict.update(Dmesons_dict)
mesons_dict.update(Chi_cmesons_dict)
mesons_dict.update(Bmesons_dict)

Nucleons_dict = {
"p" : "\Pp", # proton
"n" : "\Pn", # neutron
"ap" : "\Pap", # anti-proton
"an" : "\Pan", # anti-neutron
"proton" : "\Pp",
"neutron" : "\Pn",
"APproton" : "\Pap", "antiproton" : "\Pap",
"APneutron" : "\Pan", "antineutron" : "\Pan",
}
hepnames_dict.update(Nucleons_dict)

NucleonResonances_dict = {
"N" : "\PN",
"Na" : "\PNa",
"Nb" : "\PNb",
"Nc" : "\PNc",
"Nd" : "\PNd",
"Ne" : "\PNe",
"Nf" : "\PNf",
"Ng" : "\PNg",
"Nh" : "\PNh",
"Ni" : "\PNi",
"Nj" : "\PNj",
"Nk" : "\PNk",
"Nl" : "\PNl",
"Nm" : "\PNm",
## nice names
"nucleon" : "\PN"
}
hepnames_dict.update(NucleonResonances_dict)

DeltaBaryons_dict = {
"gD" : "\PgD",
"gDa" : "\PgDa",
"gDb" : "\PgDb",
"gDc" : "\PgDc",
"gDd" : "\PgDd",
"gDe" : "\PgDe",
"gDf" : "\PgDf",
"gDh" : "\PgDh",
"gDi" : "\PgDi",
"gDj" : "\PgDj",
"gDk" : "\PgDk"
}
hepnames_dict.update(DeltaBaryons_dict)

LambdaBaryons_dict = {
"gL" : "\PgL", # Lambda
"agL" : "\PagL", # Anti-lambda
"cgLp" : "\PcgLp", # Lambda_c
"bgL" : "\PbgL", # Lambda_b
"gLa" : "\PgLa",
"gLb" : "\PgLb",
"gLc" : "\PgLc",
"gLd" : "\PgLd",
"gLe" : "\PgLe",
"gLf" : "\PgLf",
"gLg" : "\PgLg",
"gLh" : "\PgLh",
"gLi" : "\PgLi",
"gLj" : "\PgLj",
"gLk" : "\PgLk",
"gLl" : "\PgLl",
"gLm" : "\PgLm",
## nice names
"Lambda" : "\PgL",
"APLambda" : "\PagL", "antiLambda" : "\PagL",
"Lambdac" : "\PcgLp",
"Lambdab" : "\PbgL", ## Lambda_b
}
hepnames_dict.update(LambdaBaryons_dict)

OmegaBaryons_dict = {
"gO" : "\PgO", # Omega
"gOpm" : "\PgOpm", "gOmp" : "\PgOmp", # charged Omega
"gOp" : "\PgOp", # Omega-plus
"gOm" : "\PgOm", # Omega-minus
"gOma" : "\PgOma",
"agO" : "\PagO", # anti-Omega
"agOp" : "\PagOp", # anti-Omega-plus
"agOm" : "\PagOm", # anti-Omega-minus
## nice names
"Omega" : "\PgO",
"Omegapm" : "\PgOpm", "Omegamp" : "\PgOmp",
"Omegaplus" : "\PgOp", "Omega+" : "\PgOp",
"Omegaminus" : "\PgOm", "Omega-" : "\PgOm",
"APOmega" : "\PagO", "antiOmega" : "\PagO",
"APOmegaplus" : "\PagOp", "antiOmegaplus" : "\PagOp",
"APOmega+" : "\PagOp", "antiOmega+" : "\PagOp",
"APOmegaminus" : "\PagOm", "antiOmegaminus" : "\PagOm",
"APOmega-" : "\PagOm", "antiOmega-" : "\PagOm",
}
hepnames_dict.update(OmegaBaryons_dict)

SigmaBaryons_dict = {
"gS" : "\PgS", # Sigma
"gSpm" : "\PgSpm", "gSmp" : "\PgSmp", # charged Sigma
"gSm" : "\PgSm",
"gSp" : "\PgSp",
"gSz" : "\PgSz",
"cgS" : "\PcgS",
"agSm" : "\PagSm",
"agSp" : "\PagSp",
"agSz" : "\PagSz",
"acgS" : "\PacgS",
"gSa" : "\PgSa",
"gSb" : "\PgSb",
"gSc" : "\PgSc",
"gSd" : "\PgSd",
"gSe" : "\PgSe",
"gSf" : "\PgSf",
"gSg" : "\PgSg",
"gSh" : "\PgSh",
"gSi" : "\PgSi",
"cgSi" : "\PcgSi",
## nice names
"Sigma" : "\PgS",
"Sigmapm" : "\PgSpm", "Sigmamp" : "\PgSmp",
"Sigmaminus" : "\PgSm", "Sigma-" : "\PgSm",
"Sigmaplus" : "\PgSp", "Sigma+" : "\PgSp",
"Sigmazero" : "\PgSz", "Sigma0" : "\PgSz",
"Sigmac" : "\PcgS",
"APSigmaminus" : "\PagSm", "antiSigmaminus" : "\PagSm",
"APSigma-" : "\PagSm", "antiSigma-" : "\PagSm",
"APSigmaplus" : "\PagSp", "antiSigmaplus" : "\PagSp",
"APSigma+" : "\PagSp", "antiSigma+" : "\PagSp",
"APSigmazero" : "\PagSz", "antiSigmazero" : "\PagSz",
"APSigma0" : "\PagSz", "antiSigma0" : "\PagSz",
"APSigmac" : "\PacgS", "antiSigmac" : "\PacgS"
}
hepnames_dict.update(SigmaBaryons_dict)

XiBaryons_dict = {
"gX" : "\PgX",
"gXp" : "\PgXp",
"gXm" : "\PgXm",
"gXz" : "\PgXz",
"gXa" : "\PgXa",
"gXb" : "\PgXb",
"gXc" : "\PgXc",
"gXd" : "\PgXd",
"gXe" : "\PgXe",
"agXp" : "\PagXp",
"agXm" : "\PagXm",
"agXz" : "\PagXz",
"cgXp" : "\PcgXp",
"cgXz" : "\PcgXz",
## nice names
"Xi" : "\PgX",
"Xiplus" : "\PgXp", "Xi+" : "\PgXp",
"Ximinus" : "\PgXm", "Xi-" : "\PgXm",
"Xizero" : "\PgXz", "Xi0" : "\PgXz",
"APXiplus" : "\PagXp", "antiXiplus" : "\PagXp",
"APXi+" : "\PagXp", "antiXi+" : "\PagXp",
"APXiminus" : "\PagXm", "antiXiminus" : "\PagXm",
"APXi-" : "\PagXm", "antiXi-" : "\PagXm",
"APXizero" : "\PagXz", "antiXizero" : "\PagXz",
"APXi0" : "\PagXz", "antiXi0" : "\PagXz",
"Xicplus" : "\PcgXp", "Xic+" : "\PcgXp",
"Xiczero" : "\PcgXz", "Xic0" : "\PcgXz"
}
hepnames_dict.update(XiBaryons_dict)

Baryons_dict = Nucleons_dict.copy()
Baryons_dict.update(NucleonResonances_dict)
Baryons_dict.update(DeltaBaryons_dict)
Baryons_dict.update(XiBaryons_dict)
Baryons_dict.update(SigmaBaryons_dict)
Baryons_dict.update(OmegaBaryons_dict)
Baryons_dict.update(LambdaBaryons_dict)

Hadrons_dict = mesons_dict.copy()
Hadrons_dict.update(Baryons_dict)

Gluon_dict = {
"g" : "\Pg", "gluon" : "\Pg" # gluon
}
hepnames_dict.update(Gluon_dict)

Photon_dict = {
"gg" : "\Pgg", "photon" : "\Pgg", "gamma" : "\Pgg" # photon
}
hepnames_dict.update(Photon_dict)

VectorBosons_dict = {
"W" : "\PW", # W boson
"Wpm" : "\PWpm", "Wmp" : "\PWmp", # charged W boson
"Wp" : "\PWp", # W-plus
"Wm" : "\PWm", # W-minus
"WR" : "\PWR",
"Wpr" : "\PWpr", # W-prime boson
"Z" : "\PZ", # Z boson
"Zz" : "\PZz", # neutral Z boson
"Zpr" : "\PZpr", # Z-prime boson
"ZLR" : "\PZLR", # left-right Z boson
"Zgc" : "\PZgc",
"Zge" : "\PZge",
"Zgy" : "\PZgy",
"Zi" : "\PZi",
## nice names
"Wplus" : "\PWp", "W+" : "\PWp",
"Wminus" : "\PWm", "W-" : "\PWm",
"Wprime" : "\PWpr",
"Zzero" : "\PZz", "Z0" : "\PZz", # Z with a zero
"Zprime" : "\PZpr" # Z-prime
}
hepnames_dict.update(VectorBosons_dict)

GaugeBosons_dict = Gluon_dict.copy()
GaugeBosons_dict.update(Photon_dict)
GaugeBosons_dict.update(VectorBosons_dict)

Axions_dict = {
"Az" : "\PAz", "axion" : "\PAz" # axion
}
hepnames_dict.update(Axions_dict)

Higgses_dict = {    # (inc. SUSY Higgs)
"H" : "\PH", # standard/heavy Higgs
"Hz" : "\PHz", # explicitly neutral standard/heavy Higgs
"h" : "\Ph", # light Higgs
"hz" : "\Phz", # explicitly neutral light Higgs
"A" : "\PA", # pseudoscalar Higgs
"Az" : "\PAz", # explicitly neutral pseudoscalar Higgs
"Hpm" : "\PHpm", # charged Higgs
"Hmp" : "\PHmp", # charged Higgs
"Hp" : "\PHp", # positive-charged Higgs
"Hm" : "\PHm", # negative-charged Higgs
## nice names
"Higgs" : "\PH",
"Higgsheavy" : "\PH",
"Higgslight" : "\Ph",
"Higgsheavyzero" : "\PHz", "Higgsheavy0" : "\PHz",
"Higgslightzero" : "\Phz", "Higgslight0" : "\Phz",
"Higgsps" : "\PA",
"Higgspszero" : "\PAz", "Higgsps0" : "\PAz",
"Higgsplus" : "\PHp", "Higgs+" : "\PHp",
"Higgsminus" : "\PHm", "Higgs-" : "\PHm",
"Higgspm" : "\PHpm",
"Higgsmp" : "\PHmp",
"Higgszero" : "\PHz", "Higgs0" : "\PHz"
}
hepnames_dict.update(Higgses_dict)

BasicBosons_dict = GaugeBosons_dict.copy()
BasicBosons_dict.update(Axions_dict)
BasicBosons_dict.update(Higgses_dict)

Leptons_dict = {
"l" : "\Pl", # lepton
"lpm" : "\Plpm", # charged lepton
"lmp" : "\Plmp", # charged lepton
"lp" : "\Plp", # positive lepton
"lm" : "\Plm", # negative lepton
"al" : "\Pal", # anti-lepton
"gn" : "\Pgn", # generic neutrino
"gnl" : "\Pgnl", # neutrino (for lepton \ell)
"agn" : "\Pagn", # generic anti-neutrino
"agnl" : "\Pagnl", # anti-neutrino (for lepton \ell)
"e" : "\Pe", # electronic
"epm" : "\Pepm", # e plus/minus
"emp" : "\Pemp", # e minus/plus
"em" : "\Pem", # electron
"ep" : "\Pep", # positron
"gm" : "\Pgm", # muonic
"gmpm" : "\Pgmpm", # mu plus/minus
"gmmp" : "\Pgmmp", # mu minus/plus
"gmm" : "\Pgmm", # muon
"gmp" : "\Pgmp", # anti-muon
"gt" : "\Pgt", # tauonic
"gtpm" : "\Pgtpm", # tau plus/minus
"gtmp" : "\Pgtmp", # tau minus/plus
"gtm" : "\Pgtm", # tau lepton
"gtp" : "\Pgtp", # anti-tau
"gne" : "\Pgne", # electron neutrino
"gngm" : "\Pgngm", # muon neutrino
"gngt" : "\Pgngt", # tau neutrino
"agne" : "\Pagne", # electron anti-neutrino
"agngm" : "\Pagngm", # muon anti-neutrino
"agngt" : "\Pagngt", # tau anti-neutrino
## nice names
"lepton" : "\Pl", # lepton
"leptonpm" : "\Plpm", "leptonmp" : "\Plmp", # charged lepton
"leptonplus" : "\Plp" , "lepton+" : "\Plp", # positive lepton
"leptonminus" : "\Plm" , "lepton-" : "\Plm", # negative lepton
"APlepton" : "\Pal", "antilepton" : "\Pal", # anti-lepton
"nu" : "\Pgn", # neutrino
"APnu" : "\Pagn", "antinu" : "\Pagn", # antineutrino
"neutrino" : "\Pgn", # neutrino
"APneutrino" : "\Pagn", "antineutrino" : "\Pagn", # antineutrino
"nulepton" : "\Pgnl", # l-flavour neutrino
"APnulepton" : "\Pagnl", "antinulepton" : "\Pagnl", # l-flavour antineutrino
"electron" : "\Pem", "e-": "\Pem",
"APelectron" : "\Pep", "antielectron" : "\Pep",
"positron" : "\Pep", "e+": "\Pep",
"mu" : "\Pgm",
"mupm" : "\Pgmpm", "mump" : "\Pgmmp",
"muon" : "\Pgmm", "mu-": "\Pgmm",
"APmuon" : "\Pgmp", "antimuon" : "\Pgmp", "mu+": "\Pgmp",
"tau" : "\Pgt",
"taupm" : "\Pgtpm","taump" : "\Pgtmp",
"tauon" : "\Pgtm", "tau-": "\Pgtm",
"APtauon" : "\Pgtp", "antitauon" : "\Pgtp", "tau+" : "\Pgtp",
"nue" : "\Pgne",
"num" : "\Pgngm", "numu": "\Pgngm",
"nut" : "\Pgngt", "nutau": "\Pgngt",
"APnue" : "\Pagne", "antinue" : "\Pagne",
"APnum" : "\Pagngm", "antinum" : "\Pagngm",
"APnut" : "\Pagngt", "antinut" : "\Pagngt"
}
hepnames_dict.update(Leptons_dict)

Quarks_dict = {
"q" : "\Pq", # quark
"aq" : "\Paq", # anti-quark
"qd" : "\Pqd", # down quark
"qu" : "\Pqu", # up quark
"qs" : "\Pqs", # strange quark
"qc" : "\Pqc", # charm quark
"qb" : "\Pqb", # bottom quark
"qt" : "\Pqt", # top quark
"aqd" : "\Paqd", # down anti-quark
"aqu" : "\Paqu", # up anti-quark
"aqs" : "\Paqs", # strange anti-quark
"aqc" : "\Paqc", # charm anti-quark
"aqb" : "\Paqb", # bottom anti-quark
"aqt" : "\Paqt", # top anti-quark
## nice names
"quark" : "\Pq",
"APquark" : "\Paq", "antiquark" : "\Paq",
"down" : "\Pqd",
"up" : "\Pqu",
"strange" : "\Pqs",
"charm" : "\Pqc",
"bottom" : "\Pqb",
"beauty" : "\Pqb",
"top" : "\Pqt", "truth" : "\Pqt",
"APdown" : "\Paqd", "antidown" : "\Paqd",
"APqd" : "\Paqd", "antiqd" : "\Paqd",
"APup" : "\Paqu", "antiup" : "\Paqu",
"APqu" : "\Paqu", "antiqu" : "\Paqu",
"APstrange" : "\Paqs", "antistrange" : "\Paqs",
"APqs" : "\Paqs", "antiqs" : "\Paqs",
"APcharm" : "\Paqc", "anticharm" : "\Paqc",
"APqc" : "\Paqc", "antiqc" : "\Paqc",
"APbottom" : "\Paqb", "antibottom" : "\Paqb",
"APbeauty" : "\Paqb", "antibeauty" : "\Paqb",
"APqb" : "\Paqb", "antiqb" : "\Paqb",
"APtop" : "\Paqt", "antitop" : "\Paqt",
"APtruth" : "\Paqb", "antitruth" : "\Paqb",
"APqt" : "\Paqt", "antiqt" : "\Paqt"
}
hepnames_dict.update(Quarks_dict)

BasicFermions_dict = Leptons_dict.copy()
BasicFermions_dict.update(Quarks_dict)

AllFermions_dict = BasicFermions_dict.copy()
AllFermions_dict.update(Baryons_dict)

AllBosons_dict = BasicBosons_dict.copy()
AllBosons_dict.update(mesons_dict)

MiscParticles_dict = {
"Ez" : "\PEz",
"Lpm" : "\PLpm",
"Lmp" : "\PLmp",
"Lz" : "\PLz",
}
hepnames_dict.update(MiscParticles_dict)

Ghost_dict = {"ghost" : ""} # Fadeev-Popov ghosts (needed for internal lines)

SUSYparticles_dict = {
"SH" : "\PSH", # Higgsino
"SHp" : "\PSHp", # positive Higgsino
"SHm" : "\PSHm", # negative Higgsino
"SHpm" : "\PSHpm", "SHmp" : "\PSHmp", # charged Higgsino
"SHz" : "\PSHz", # neutral Higgsino
"SW" : "\PSW", # wino
"SWp" : "\PSWp", # positive wino
"SWm" : "\PSWm", # negative wino
"SWpm" : "\PSWpm", "SWmp" : "\PSWmp", # charged wino
"SZ" : "\PSZ", # zino
"SZz" : "\PSZz", # neutral zino
"SB" : "\PSB", # bino
"Se" : "\PSe", # selectron
"Sgg" : "\PSgg", # photino
"Sgm" : "\PSgm", # smuon
"Sgn" : "\PSgn", # sneutrino
"Sgt" : "\PSgt", # stau
"Sgx" : "\PSgx", # chargino/neutralino
"Sgxpm" : "\PSgxpm", "Sgxmp" : "\PSgxmp", # charged chargino
"Sgxz" : "\PSgxz", # neutralino
"Sgxzi" : "\PSgxzi", # lightest neutralino
"Sgxzii" : "\PSgxzii", # next-to-lightest neutralino
"Sg" : "\PSg", # gluino
"Sl" : "\PSl", # slepton (generic)
"aSl" : "\PaSl", # anti-slepton (generic)
"Sq" : "\PSq", # squark (generic)
"aSq" : "\PaSq", # anti-squark (generic)
"Sqd" : "\PSqd", # down squark
"Squ" : "\PSqu", # up squark
"Sqs" : "\PSqs", # strange squark
"Sqc" : "\PSqc", # charm squark
"Sqb" : "\PSqb", # bottom squark (sbottom)
"Sqt" : "\PSqt", # top squark (stop)
"aSqd" : "\PaSqd", # anti-down squark
"aSqu" : "\PaSqu", # anti-up squark
"aSqs" : "\PaSqs", # anti-strange squark
"aSqc" : "\PaSqc", # anti-charm squark
"aSqb" : "\PaSqb", # anti-bottom squark
"aSqt" : "\PaSqt", # anti-top squark (stop)
## nice names
"SHiggs" : "\PSH", "SHiggsino" : "\PSH", "Higgsino" : "\PSH",
"SHiggsplus" : "\PSHp", "SHiggs+" : "\PSHp",
"SHiggsinoplus" : "\PSHp", "SHiggsino+" : "\PSHp",
"Higgsinoplus" : "\PSHp", "Higgsino+" : "\PSHp",
"SHiggsminus" : "\PSHm", "SHiggs-" : "\PSHm",
"SHiggsinominus" : "\PSHm", "SHiggsino-" : "\PSHm",
"Higgsinominus" : "\PSHm", "Higgsino-" : "\PSHm",
"SHiggspm" : "\PSHpm", "SHiggsinopm" : "\PSHpm", "Higgsinopm" : "\PSHpm",
"SHiggsmp" : "\PSHmp", "SHiggsinomp" : "\PSHmp", "Higgsinomp" : "\PSHmp",
"SHiggszero" : "\PSHz", "SHiggs0" : "\PSHz",
"SHiggsinozero" : "\PSHz", "SHiggsino0" : "\PSHz",
"Higgsinozero" : "\PSHz", "Higgsino0" : "\PSHz",
"SBino" : "\PSB", # bino,
"Bino" : "\PSB",
"SWplus" : "\PSWp" , "SW+" : "\PSWp", # wino
"SWminus" : "\PSWm" , "SW-" : "\PSWm",
"SWino" : "\PSW", "Wino" : "\PSW", 
"SWinopm" : "\PSWpm", "Winopm" : "\PSWpm", 
"SWinomp" : "\PSWmp", "Winomp" : "\PSWmp", 
"SZzero" : "\PSZz", "SZ0" : "\PSZz",
"Sphoton" : "\PSgg", # photino
"Sphotino" : "\PSgg",
"photino" : "\PSgg", 
"Smu" : "\PSgm", # smuon
"Snu" : "\PSgn", # sneutrino
"Stau" : "\PSgt", # stau
"Sino" : "\PSgx", # neutralino/chargino
"Scharginopm" : "\PSgxpm", "Scharginomp" : "\PSgxmp", # chargino
"charginopm" : "\PSgxpm", "charginomp" : "\PSgxmp", # chargino
"Sneutralino" : "\PSgxz", # neutralino
"neutralino" : "\PSgxz",
"SneutralinoOne" : "\PSgxzi", # lightest neutralino
"neutralinoOne" : "\PSgxzi", 
"SneutralinoTwo" : "\PSgxzii", # next-to-lightest neutralino
"neutralinoTwo" : "\PSgxzii",
"Sgluino" : "\PSg", "gluino" : "\PSg", # gluino
"Slepton" : "\PSl", "slepton" : "\PSl", # slepton
"APSlepton" : "\PaSl", "antiSlepton" : "\PaSl", # anti-slepton
"APslepton" : "\PaSl", "antislepton" : "\PaSl",
"squark" : "\PSq", # squarks
"APSq" : "\PaSq", "antiSq" : "\PaSq",
"APsquark" : "\PaSq", "antisquark" : "\PaSq",
"Sdown" : "\PSqd",
"Sup" : "\PSqu",
"Sstrange" : "\PSqs",
"Scharm" : "\PSqc",
"Sbottom" : "\PSqb",
"Stop" : "\PSqt",
"ASdown" : "\PaSqd", "antiSdown" : "\PaSqd", # antisquarks
"ASup" : "\PaSqu", "antiSup" : "\PaSqu",
"ASstrange" : "\PaSqs", "antiSstrange" : "\PaSqs",
"AScharm" : "\PaSqc", "antiScharm" : "\PaSqc",
"ASbottom" : "\PaSqb", "antiSbottom" : "\PaSqb",
"AStop" : "\PaSqt", "antiStop" : "\PaSqt"
}
hepnames_dict.update(SUSYparticles_dict)


## Gauge boson type testing

def is_photon(name):
    return Photon_dict.has_key(name)

def is_gluon(name):
    return Gluon_dict.has_key(name)

def is_weakboson(name):
    return VectorBosons_dict.has_key(name)

def is_gauge(name):
    return is_photon(name) or is_gluon(name) or is_weakboson(name)

## Higgs boson type testing

def is_higgs(name):
    return Higgses_dict.has_key(name)

## Fermion type testing

def is_quark(name):
    return Quarks_dict.has_key(name)

def is_lepton(name):
    return Leptons_dict.has_key(name)

def is_quark_lepton(name):
    return is_quark(name) or is_lepton(name)

## Hadron type testing

def is_meson(name):
    return mesons_dict.has_key(name)

def is_baryon(name):
    return Baryons_dict.has_key(name)

def is_hadron(name):
    return Hadrons_dict.has_key(name)

## Other type tests

def is_ghost(name):
    return Ghost_dict.has_key(name)

## Classify particle according to its coarse physical type

def hep_classify(name):
    if is_ghost(name):
        return "ghost"
    elif is_meson(name):
        return "meson"
    elif is_baryon(name):
        return "baryon"
    elif is_quark(name):
        return "quark"
    elif is_lepton(name):
        return "lepton"
    elif is_higgs(name):
        return "higgs boson"
    elif is_gauge(name):
        return "gauge boson"
    else:
        return "other particle"

## Classify particle according to the linestyle to use when drawing

def hep_linestyle(name):
    if is_ghost(name):
        return "ghost" # dotted or dashed
    elif is_meson(name):
        return "meson" # dashed, dotted, solid or double
    elif is_baryon(name):
        return "baryon" # solid or double
    elif is_quark_lepton(name):
        return "fermion" # solid (sometimes double if heavy)
    elif is_higgs(name):
        return "higgs" # usually dashed
    elif is_photon(name):
        return "photon" # wavy
    elif is_gluon(name):
        return "gluon" # curly
    elif is_weakboson(name):
        return "weak" # wavy or zigzag
    else:
        return "ask_user" # can't determine automatically

