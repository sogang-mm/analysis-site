#!/usr/bin/env bash
celery -A AnalysisSite worker -B -l info
