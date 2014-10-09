"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy
import thinkbayes2
import thinkplot


class Football(thinkbayes2.Suite):
    """Represents hypotheses about."""

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: hypothetical goal scoring rate in goals per game
        data: time between goals in minutes

        x=quantity where evaluating print_function
        lam=parameter determining rate in events/unit time
        """
        x = data #time between goals in minutes
        lam = hypo/60 #time per minute: the 11 in the update is 11 minutes into the game
        like = thinkbayes2.EvalExponentialPdf(x,lam) #evaluating for every value of lamda
        return like

    def PredRemaining(self, rem_time, score):
        """Plots the predictive distribution for final number of goals.

        rem_time: remaining time in the game in minutes
        score: number of goals already scored
        """
        metapmf=thinkbayes2.Pmf() #PMF about PMFS. probabilities of pmf values
        for lam, prob in self.Items(): #loop through probabilities of lamdas
            #print(lam,prob)
            lt = lam*rem_time/60
            pmf=thinkbayes2.MakePoissonPmf(lt,20)
            #thinkplot.Pdf(pmf,linewidth=1,alpha=0.2,color='purple')
            metapmf[pmf]=prob

        mix = thinkbayes2.MakeMixture(metapmf)
        mix += score #shift by 2 because we've already seen 2
        return mix

def constructPriors():
    meanFG=1.647
    meanTD=2.397
    FGtime=60/meanFG
    TDtime=60/meanTD

    hyposFG = numpy.linspace(0, 20, 201)
    suiteFG = Football(hyposFG)

    hyposTD = numpy.linspace(0, 20, 201)
    suiteTD = Football(hyposTD)

    thinkplot.Pdf(suiteFG, label='priorFG')
    print('Field Goal prior mean', suiteFG.Mean())
    thinkplot.Pdf(suiteFG, label='priorTD')
    print('Touchdown prior mean', suiteTD.Mean())

    ##construct priors using pseudo-observation
    suiteFG.Update(FGtime)
    suiteTD.Update(TDtime)

    thinkplot.Pdf(suiteFG, label='prior 2: FG pseudo-observation')
    print('pseudo-observation', suiteFG.Mean())
    thinkplot.Pdf(suiteTD, label='prior 2: TD pseudo-observation')
    print('pseudo-observation', suiteTD.Mean())

    thinkplot.Show()

    return suiteTD, suiteFG


def main():

    suiteTD, suiteFG = constructPriors()

    #if we know what lamda is, we know the goals left in the game.
    FGpredict=suiteFG.PredRemaining(60,0)
    TDpredict=suiteTD.PredRemaining(60,0)
    GoalTotal=FGpredict*3+TDpredict*7
    thinkplot.Clf()
    #thinkplot.Hist(FGpredict)
    #thinkplot.Hist(TDpredict)
    thinkplot.Hist(GoalTotal)
    thinkplot.Show()

if __name__ == '__main__':
    main()
