#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_decisionTable
----------------------------------

Tests for `decisionTable` module.
"""

import unittest

import decisionTable


class TestDecisionTable(unittest.TestCase):

    #Overriden
    def setUp(self):
        self.table = decisionTable.DecisionTable("""

        packageState     configState     config        action        new_packageState    new_configState

        ================================================================================================
        None             None            False         install       install             install            
        ok               ok              False         purge         purge               purge

        .                .               True          purge         ok                  purge
        .                .               True          update        ok                  update
        ok               error           False         purge         purge               purge

        .                .               True          update        ok                  update
        .                .               True          install       ok                  install
        .                .               True          purge         ok                  purge
        error            install         False         purge         purge               purge
        .                .               False         install       install             install
        None             error           True          purge         None                purge
        error            purge           False         purge         purge               purge
        ok               None            True          install       ok                  install
        .                .               False         purge         purge               None
        *                *               *             *             ERROR               ERROR
        
            """)

        
    def test_variable_header(self):
        self.assertIsNotNone(self.table.header)
        self.assertEqual(self.table.header,[
            'packageState',
            'configState',
            'config',
            'action',
            'new_packageState',
            'new_configState'
        ])
    
    def test_variable_decisions(self):
        self.assertIsNotNone(self.table.decisions)
        self.assertEqual(self.table.decisions,
            [
                ['None', 'None', 'False', 'install', 'install', 'install'],
                ['ok', 'ok', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'ok', 'True', 'purge', 'ok', 'purge'],
                ['ok', 'ok', 'True', 'update', 'ok', 'update'],
                ['ok', 'error', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'error', 'True', 'update', 'ok', 'update'],
                ['ok', 'error', 'True', 'install', 'ok', 'install'],
                ['ok', 'error', 'True', 'purge', 'ok', 'purge'],
                ['error', 'install', 'False', 'purge', 'purge', 'purge'],
                ['error', 'install', 'False', 'install', 'install', 'install'],
                ['None', 'error', 'True', 'purge', 'None', 'purge'],
                ['error', 'purge', 'False', 'purge', 'purge', 'purge'],
                ['ok', 'None', 'True', 'install', 'ok', 'install'],
                ['ok', 'None', 'False', 'purge', 'purge', 'None'],
                ['*', '*', '*', '*', 'ERROR', 'ERROR']
            ]
        )
    
    def test_method_decisionCall(self):
        this = self
        
        def testCallback(new_packageState,new_configState):
            this.assertEqual(new_packageState,'ok')
            this.assertEqual(new_configState,'purge')
        
        self.table.decisionCall(testCallback,
            ['new_packageState','new_configState'],
            packageState = 'ok',
            configState = 'error',
            config = True,
            action = 'purge'
        )
    
    def test_method_decision(self):
        result = self.table.decision(
            ['new_packageState','new_configState'],
            packageState = 'error',
            configState = 'install',
            config = 'False',
            action = 'install'
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result,['install','install'])
    
    def test_method_allDecision(self):
        result = self.table.allDecisions(
            ['new_packageState','new_configState'],
            packageState = 'error'
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result,
            [
                ['purge','install','purge','ERROR'],
                ['purge','install','purge','ERROR']
            ]
        )
        
    #Overriden
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
