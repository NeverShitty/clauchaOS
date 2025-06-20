#!/usr/bin/env python3
"""
🎯 CLAUDE MEMORY AUTOMATED INSIGHTS GENERATOR
Generates weekly/monthly reports from memory data with subscription service capabilities
"""

import os
import json
import openai
import subprocess
from datetime import datetime, timedelta
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import boto3
import stripe
import schedule
import time
import logging
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get OpenAI API key
try:
    api_key = subprocess.run(
        ['op', 'item', 'get', 'bazgqwkfs7lytomdk2nrw46lbi', '--fields', 'claucha_os_api_key'],
        capture_output=True, text=True
    ).stdout.strip()
except:
    api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

# Vector store and assistant IDs
VECTOR_STORE_ID = "vs_684f6a5c90088191ac179ac2af2cc82c"
ASSISTANT_IDS = {
    "METACLAUDE": "asst_LXYH3RHmmkb60whOB236g1d4",
    "CLAUDEFO": "asst_cjYrAuq4E8AQozDj6Xzz84Yc",
    "CLAUDESQ": "asst_tkBVT2u44lFI2Sx8i4oxDUvk",
    "CLAUDALYN": "asst_jj4cciM6w71iTAb9y7zCQmME",
    "CLAUDEMOM": "asst_I83wmISGknCCcovr29U6wHPc",
    "CLAUDEMO": "asst_cytoTn1hRG5dwc8hjg26fXM9",
    "CLAUDESQUAD": "asst_AHrrV087yro1A7J7tr5kKIfc",
    "CLAUDEXTER": "asst_o7zobHOw4v5LkvBS38W3JDzq",
    "CLAUDEBABY": "asst_PobIZnA556lkKeME0yy6LYc6",
    "CLAUDETTE": "asst_hs4gH6YrhMwNUaf0vb37JANX",
    "CLAUDADDY": "asst_U6DebcIE2x7XYc0HyJupcygD"
}

class MemoryInsightsGenerator:
    def __init__(self, base_path="/Users/nickbianchi/MCMANSION/AUTOMATION_LAB"):
        self.base_path = base_path
        self.memory_dir = os.path.join(base_path, "vector_memory_v3")
        self.reports_dir = os.path.join(base_path, "insights_reports")
        self.subscribers_file = os.path.join(self.memory_dir, "subscribers.json")
        self.analytics_file = os.path.join(self.memory_dir, "analytics_cache.json")
        
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Load subscribers
        self.subscribers = self._load_json(self.subscribers_file) or {
            "weekly": [],
            "monthly": [],
            "custom": []
        }
        
        # Analytics cache
        self.analytics_cache = self._load_json(self.analytics_file) or {}
        
        # Report templates
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30
        )
        
    def _load_json(self, filepath):
        """Load JSON file safely"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def _save_json(self, data, filepath):
        """Save JSON file with backup"""
        backup_path = filepath + '.backup'
        if os.path.exists(filepath):
            os.rename(filepath, backup_path)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def analyze_memory_patterns(self, period="week"):
        """Analyze memory patterns for insights"""
        logger.info(f"Analyzing memory patterns for {period}")
        
        # Calculate date range
        end_date = datetime.now()
        if period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=period)
        
        analysis = {
            "period": period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "instance_activity": {},
            "top_patterns": [],
            "qa_scores": {},
            "knowledge_gaps": [],
            "proactive_predictions": [],
            "improvement_tracking": [],
            "financial_insights": {},
            "legal_alerts": [],
            "automation_savings": {},
            "adhd_patterns": {}
        }
        
        # Query each assistant for their memories
        for instance, assistant_id in ASSISTANT_IDS.items():
            if instance == "CLAUDEMOM":  # Skip private
                continue
                
            memories = self._query_assistant_memories(assistant_id, instance, start_date, end_date)
            analysis["instance_activity"][instance] = self._analyze_instance_activity(memories, instance)
        
        # Extract patterns
        analysis["top_patterns"] = self._extract_top_patterns(analysis["instance_activity"])
        
        # Calculate QA scores
        analysis["qa_scores"] = self._calculate_qa_scores(analysis["instance_activity"])
        
        # Identify knowledge gaps
        analysis["knowledge_gaps"] = self._identify_knowledge_gaps(analysis["instance_activity"])
        
        # Generate predictions
        analysis["proactive_predictions"] = self._generate_predictions(analysis)
        
        # Financial insights
        if "CLAUDEFO" in analysis["instance_activity"]:
            analysis["financial_insights"] = self._extract_financial_insights(
                analysis["instance_activity"]["CLAUDEFO"]
            )
        
        # Legal alerts
        if "CLAUDESQ" in analysis["instance_activity"]:
            analysis["legal_alerts"] = self._extract_legal_alerts(
                analysis["instance_activity"]["CLAUDESQ"]
            )
        
        # Automation savings
        if "CLAUDETTE" in analysis["instance_activity"]:
            analysis["automation_savings"] = self._calculate_automation_savings(
                analysis["instance_activity"]["CLAUDETTE"]
            )
        
        # ADHD patterns
        analysis["adhd_patterns"] = self._analyze_adhd_patterns(analysis["instance_activity"])
        
        # Cache results
        cache_key = f"{period}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        self.analytics_cache[cache_key] = analysis
        self._save_json(self.analytics_cache, self.analytics_file)
        
        return analysis
    
    def _query_assistant_memories(self, assistant_id, instance, start_date, end_date):
        """Query assistant for memories in date range"""
        try:
            thread = client.beta.threads.create()
            
            # Query for memories
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"Search memories from {start_date.strftime('%Y%m%d')} to {end_date.strftime('%Y%m%d')} and return with QA scores, patterns, and insights"
            )
            
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )
            
            # Wait for completion
            while run.status not in ["completed", "failed"]:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                return self._parse_assistant_response(messages.data[0].content[0].text.value)
            
        except Exception as e:
            logger.error(f"Error querying {instance}: {e}")
            
        return []
    
    def _analyze_instance_activity(self, memories, instance):
        """Analyze activity for a specific instance"""
        activity = {
            "total_memories": len(memories),
            "conversations": 0,
            "qa_scores": {"speed": [], "accuracy": [], "authenticity": [], "usefulness": []},
            "common_topics": Counter(),
            "peak_hours": Counter(),
            "improvements": [],
            "patterns": []
        }
        
        for memory in memories:
            # Extract QA scores
            if "qa_scores" in memory:
                for metric, score in memory["qa_scores"].items():
                    if metric in activity["qa_scores"]:
                        activity["qa_scores"][metric].append(score)
            
            # Track topics
            if "topics" in memory:
                for topic in memory["topics"]:
                    activity["common_topics"][topic] += 1
            
            # Track time patterns
            if "timestamp" in memory:
                hour = datetime.fromisoformat(memory["timestamp"]).hour
                activity["peak_hours"][hour] += 1
        
        # Calculate averages
        for metric in activity["qa_scores"]:
            scores = activity["qa_scores"][metric]
            if scores:
                activity["qa_scores"][metric] = sum(scores) / len(scores)
            else:
                activity["qa_scores"][metric] = 0
        
        return activity
    
    def _extract_top_patterns(self, instance_activity):
        """Extract top patterns across all instances"""
        all_topics = Counter()
        
        for instance, activity in instance_activity.items():
            all_topics.update(activity["common_topics"])
        
        return [
            {"pattern": topic, "frequency": count, "impact": self._assess_pattern_impact(topic, count)}
            for topic, count in all_topics.most_common(10)
        ]
    
    def _calculate_qa_scores(self, instance_activity):
        """Calculate aggregated QA scores"""
        qa_scores = {}
        
        for instance, activity in instance_activity.items():
            qa_scores[instance] = activity["qa_scores"]
        
        return qa_scores
    
    def _identify_knowledge_gaps(self, instance_activity):
        """Identify gaps in knowledge or slow response areas"""
        gaps = []
        
        for instance, activity in instance_activity.items():
            # Low QA scores indicate gaps
            qa_scores = activity["qa_scores"]
            
            if qa_scores["accuracy"] < 8:
                gaps.append({
                    "instance": instance,
                    "gap_type": "accuracy",
                    "score": qa_scores["accuracy"],
                    "recommendation": f"Review and update {instance} knowledge base"
                })
            
            if qa_scores["speed"] < 7:
                gaps.append({
                    "instance": instance,
                    "gap_type": "speed",
                    "score": qa_scores["speed"],
                    "recommendation": f"Optimize {instance} response patterns"
                })
        
        return gaps
    
    def _generate_predictions(self, analysis):
        """Generate predictive insights"""
        predictions = []
        
        # Analyze patterns for predictions
        for pattern in analysis["top_patterns"][:5]:
            if pattern["frequency"] > 10:
                predictions.append({
                    "prediction": f"High likelihood of continued {pattern['pattern']} queries",
                    "confidence": min(0.9, pattern["frequency"] / 50),
                    "recommendation": f"Prepare proactive documentation for {pattern['pattern']}"
                })
        
        # Financial predictions
        if analysis["financial_insights"]:
            if "growth_rate" in analysis["financial_insights"]:
                rate = analysis["financial_insights"]["growth_rate"]
                predictions.append({
                    "prediction": f"Revenue trend indicates {rate:.1%} growth next period",
                    "confidence": 0.75,
                    "recommendation": "Update financial projections"
                })
        
        return predictions
    
    def _extract_financial_insights(self, fo_activity):
        """Extract financial insights from CLAUDEFO"""
        insights = {
            "total_transactions": fo_activity["total_memories"],
            "patterns": [],
            "alerts": [],
            "opportunities": []
        }
        
        # Look for value patterns
        for topic, count in fo_activity["common_topics"].most_common(5):
            if "$" in topic or any(keyword in topic.lower() for keyword in ["revenue", "expense", "profit"]):
                insights["patterns"].append({
                    "pattern": topic,
                    "frequency": count
                })
        
        return insights
    
    def _extract_legal_alerts(self, sq_activity):
        """Extract legal alerts from CLAUDESQ"""
        alerts = []
        
        for topic, count in sq_activity["common_topics"].items():
            if any(keyword in topic.lower() for keyword in ["deadline", "filing", "court", "motion"]):
                alerts.append({
                    "alert": topic,
                    "urgency": "high" if "deadline" in topic.lower() else "medium",
                    "frequency": count
                })
        
        return sorted(alerts, key=lambda x: x["urgency"], reverse=True)
    
    def _calculate_automation_savings(self, ette_activity):
        """Calculate time/cost savings from automation"""
        savings = {
            "total_automations": ette_activity["total_memories"],
            "time_saved_hours": 0,
            "cost_saved_estimate": 0,
            "top_automations": []
        }
        
        # Estimate based on automation patterns
        for topic in ette_activity["common_topics"]:
            if "save" in topic.lower() or "automat" in topic.lower():
                # Extract time savings if mentioned
                import re
                time_match = re.search(r'(\d+)\s*(hour|hr|min)', topic.lower())
                if time_match:
                    value = int(time_match.group(1))
                    unit = time_match.group(2)
                    hours = value if 'hour' in unit or 'hr' in unit else value / 60
                    savings["time_saved_hours"] += hours
        
        # Estimate cost savings at $100/hour
        savings["cost_saved_estimate"] = savings["time_saved_hours"] * 100
        
        return savings
    
    def _analyze_adhd_patterns(self, instance_activity):
        """Analyze ADHD-related patterns"""
        patterns = {
            "peak_productivity": {},
            "distraction_patterns": [],
            "hyperfocus_topics": [],
            "recommended_strategies": []
        }
        
        # Aggregate peak hours across instances
        all_hours = Counter()
        for activity in instance_activity.values():
            all_hours.update(activity["peak_hours"])
        
        # Find peak productivity windows
        top_hours = all_hours.most_common(3)
        patterns["peak_productivity"] = {
            str(hour): count for hour, count in top_hours
        }
        
        # Identify hyperfocus topics (high frequency in short time)
        for instance, activity in instance_activity.items():
            for topic, count in activity["common_topics"].items():
                if count > 5:  # High frequency suggests hyperfocus
                    patterns["hyperfocus_topics"].append({
                        "topic": topic,
                        "instance": instance,
                        "intensity": count
                    })
        
        # Generate strategies
        if patterns["peak_productivity"]:
            peak_hour = list(patterns["peak_productivity"].keys())[0]
            patterns["recommended_strategies"].append(
                f"Schedule important work during peak hour: {peak_hour}:00"
            )
        
        return patterns
    
    def _assess_pattern_impact(self, pattern, frequency):
        """Assess the business impact of a pattern"""
        high_impact_keywords = ["revenue", "deadline", "contract", "deploy", "error", "urgent"]
        
        impact_score = frequency
        for keyword in high_impact_keywords:
            if keyword in pattern.lower():
                impact_score *= 2
        
        if impact_score > 50:
            return "critical"
        elif impact_score > 20:
            return "high"
        elif impact_score > 10:
            return "medium"
        else:
            return "low"
    
    def _parse_assistant_response(self, response_text):
        """Parse assistant response into structured data"""
        memories = []
        
        try:
            # Parse response looking for tagged memories
            lines = response_text.split('\n')
            current_memory = {}
            
            for line in lines:
                if line.startswith('[#'):
                    if current_memory:
                        memories.append(current_memory)
                    
                    # Extract tag and content
                    tag_end = line.find(']')
                    if tag_end > 0:
                        tag = line[1:tag_end]
                        content = line[tag_end + 1:].strip()
                        
                        # Parse timestamp from tag
                        parts = tag.split('_')
                        if len(parts) >= 3:
                            date_str = parts[1]
                            time_str = parts[2]
                            timestamp = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                            
                            current_memory = {
                                "tag": tag,
                                "content": content,
                                "timestamp": timestamp.isoformat(),
                                "instance": parts[0].replace('#', '')
                            }
                
                # Look for QA scores
                elif "Speed:" in line and current_memory:
                    scores = {}
                    score_parts = line.split(',')
                    for part in score_parts:
                        if ':' in part:
                            metric, value = part.split(':')
                            metric = metric.strip().lower()
                            try:
                                scores[metric] = float(value.strip().split('/')[0])
                            except:
                                pass
                    current_memory["qa_scores"] = scores
                
                # Extract topics from content
                elif current_memory and "content" in current_memory:
                    # Simple topic extraction
                    words = current_memory["content"].lower().split()
                    topics = [w for w in words if len(w) > 4 and not w.startswith('http')]
                    current_memory["topics"] = topics[:5]
            
            # Don't forget the last memory
            if current_memory:
                memories.append(current_memory)
                
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
        
        return memories
    
    def generate_report(self, analysis, format="pdf"):
        """Generate formatted report from analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        period_name = analysis["period"]
        
        if format == "pdf":
            filename = f"claude_insights_{period_name}_{timestamp}.pdf"
            filepath = os.path.join(self.reports_dir, filename)
            self._generate_pdf_report(analysis, filepath)
        elif format == "html":
            filename = f"claude_insights_{period_name}_{timestamp}.html"
            filepath = os.path.join(self.reports_dir, filename)
            self._generate_html_report(analysis, filepath)
        else:
            filename = f"claude_insights_{period_name}_{timestamp}.json"
            filepath = os.path.join(self.reports_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(analysis, f, indent=2)
        
        logger.info(f"Report generated: {filepath}")
        return filepath
    
    def _generate_pdf_report(self, analysis, filepath):
        """Generate PDF report with charts"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(f"Claude Memory Insights Report", self.title_style)
        story.append(title)
        
        period_text = f"{analysis['start_date'][:10]} to {analysis['end_date'][:10]}"
        subtitle = Paragraph(f"Period: {period_text}", self.styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.5 * inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['Heading2']))
        
        total_memories = sum(act["total_memories"] for act in analysis["instance_activity"].values())
        summary_text = f"""
        <para>
        Total Memories Processed: <b>{total_memories}</b><br/>
        Active Instances: <b>{len(analysis['instance_activity'])}</b><br/>
        Top Patterns Identified: <b>{len(analysis['top_patterns'])}</b><br/>
        Knowledge Gaps Found: <b>{len(analysis['knowledge_gaps'])}</b><br/>
        Proactive Predictions: <b>{len(analysis['proactive_predictions'])}</b>
        </para>
        """
        story.append(Paragraph(summary_text, self.styles['BodyText']))
        story.append(Spacer(1, 0.3 * inch))
        
        # QA Performance Scores
        story.append(Paragraph("Quality Assurance Scores", self.styles['Heading2']))
        
        qa_data = [["Instance", "Speed", "Accuracy", "Authenticity", "Usefulness"]]
        for instance, scores in analysis["qa_scores"].items():
            if isinstance(scores, dict):
                qa_data.append([
                    instance,
                    f"{scores.get('speed', 0):.1f}/10",
                    f"{scores.get('accuracy', 0):.1f}/10",
                    f"{scores.get('authenticity', 0):.1f}/10",
                    f"{scores.get('usefulness', 0):.1f}/10"
                ])
        
        qa_table = Table(qa_data)
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(qa_table)
        story.append(PageBreak())
        
        # Top Patterns
        story.append(Paragraph("Top Memory Patterns", self.styles['Heading2']))
        
        for i, pattern in enumerate(analysis["top_patterns"][:5], 1):
            pattern_text = f"""
            <para>
            <b>{i}. {pattern['pattern']}</b><br/>
            Frequency: {pattern['frequency']} | Impact: <font color="{'red' if pattern['impact'] == 'critical' else 'orange' if pattern['impact'] == 'high' else 'black'}">{pattern['impact']}</font>
            </para>
            """
            story.append(Paragraph(pattern_text, self.styles['BodyText']))
            story.append(Spacer(1, 0.1 * inch))
        
        # Financial Insights (if available)
        if analysis["financial_insights"]:
            story.append(Paragraph("Financial Insights", self.styles['Heading2']))
            fin_insights = analysis["financial_insights"]
            
            if "cost_saved_estimate" in analysis.get("automation_savings", {}):
                savings = analysis["automation_savings"]["cost_saved_estimate"]
                financial_text = f"""
                <para>
                Automation Cost Savings: <b>${savings:,.2f}</b><br/>
                Time Saved: <b>{analysis['automation_savings'].get('time_saved_hours', 0):.1f} hours</b>
                </para>
                """
                story.append(Paragraph(financial_text, self.styles['BodyText']))
        
        # Legal Alerts
        if analysis["legal_alerts"]:
            story.append(Paragraph("Legal Alerts", self.styles['Heading2']))
            
            for alert in analysis["legal_alerts"][:3]:
                alert_color = "red" if alert["urgency"] == "high" else "orange"
                alert_text = f"""
                <para>
                <font color="{alert_color}">⚠️ {alert['alert']}</font><br/>
                Urgency: {alert['urgency']} | Mentions: {alert['frequency']}
                </para>
                """
                story.append(Paragraph(alert_text, self.styles['BodyText']))
                story.append(Spacer(1, 0.1 * inch))
        
        # Predictions
        story.append(PageBreak())
        story.append(Paragraph("Predictive Insights", self.styles['Heading2']))
        
        for pred in analysis["proactive_predictions"][:5]:
            confidence_pct = pred["confidence"] * 100
            pred_text = f"""
            <para>
            <b>Prediction:</b> {pred['prediction']}<br/>
            <b>Confidence:</b> {confidence_pct:.0f}%<br/>
            <b>Recommendation:</b> {pred['recommendation']}
            </para>
            """
            story.append(Paragraph(pred_text, self.styles['BodyText']))
            story.append(Spacer(1, 0.2 * inch))
        
        # ADHD Insights
        if analysis["adhd_patterns"]:
            story.append(Paragraph("ADHD Pattern Analysis", self.styles['Heading2']))
            
            adhd = analysis["adhd_patterns"]
            if adhd["peak_productivity"]:
                peak_hours = ", ".join([f"{h}:00" for h in adhd["peak_productivity"].keys()])
                adhd_text = f"""
                <para>
                <b>Peak Productivity Hours:</b> {peak_hours}<br/>
                <b>Hyperfocus Topics:</b> {len(adhd.get('hyperfocus_topics', []))} identified<br/>
                <b>Recommended Strategies:</b><br/>
                """
                
                for strategy in adhd.get("recommended_strategies", []):
                    adhd_text += f"• {strategy}<br/>"
                
                adhd_text += "</para>"
                story.append(Paragraph(adhd_text, self.styles['BodyText']))
        
        # Knowledge Gaps
        if analysis["knowledge_gaps"]:
            story.append(Paragraph("Knowledge Gap Analysis", self.styles['Heading2']))
            
            gap_data = [["Instance", "Gap Type", "Score", "Recommendation"]]
            for gap in analysis["knowledge_gaps"]:
                gap_data.append([
                    gap["instance"],
                    gap["gap_type"],
                    f"{gap['score']:.1f}/10",
                    gap["recommendation"]
                ])
            
            gap_table = Table(gap_data, colWidths=[1.5*inch, 1*inch, 1*inch, 3*inch])
            gap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(gap_table)
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        footer_text = f"""
        <para fontSize="8" alignment="center">
        Generated by Claude Memory Insights System<br/>
        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        © ChittyStacks - Powered by OpenAI & Claude
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
    
    def _generate_html_report(self, analysis, filepath):
        """Generate HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Claude Memory Insights Report</title>
            <style>
                body {{ font-family: -apple-system, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #1a1a1a; }}
                h2 {{ color: #333; margin-top: 30px; }}
                .metric {{ background: #f0f0f0; padding: 20px; border-radius: 5px; margin: 10px 0; }}
                .metric-value {{ font-size: 36px; font-weight: bold; color: #4CAF50; }}
                .qa-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .qa-table th, .qa-table td {{ padding: 12px; text-align: center; border: 1px solid #ddd; }}
                .qa-table th {{ background: #333; color: white; }}
                .alert {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .alert.high {{ background: #f8d7da; border-color: #f5c6cb; }}
                .prediction {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .confidence {{ font-weight: bold; color: #0c5460; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Claude Memory Insights Report</h1>
                <p>Period: {analysis['start_date'][:10]} to {analysis['end_date'][:10]}</p>
                
                <h2>Executive Summary</h2>
                <div class="metric">
                    <div>Total Memories Processed</div>
                    <div class="metric-value">{sum(act['total_memories'] for act in analysis['instance_activity'].values())}</div>
                </div>
                
                <h2>Quality Assurance Scores</h2>
                <table class="qa-table">
                    <tr>
                        <th>Instance</th>
                        <th>Speed</th>
                        <th>Accuracy</th>
                        <th>Authenticity</th>
                        <th>Usefulness</th>
                    </tr>
        """
        
        # Add QA scores
        for instance, activity in analysis["instance_activity"].items():
            scores = activity.get("qa_scores", {})
            html_content += f"""
                    <tr>
                        <td>{instance}</td>
                        <td>{scores.get('speed', 0):.1f}/10</td>
                        <td>{scores.get('accuracy', 0):.1f}/10</td>
                        <td>{scores.get('authenticity', 0):.1f}/10</td>
                        <td>{scores.get('usefulness', 0):.1f}/10</td>
                    </tr>
            """
        
        html_content += """
                </table>
                
                <h2>Top Patterns</h2>
        """
        
        # Add patterns
        for pattern in analysis["top_patterns"][:5]:
            html_content += f"""
                <div class="metric">
                    <strong>{pattern['pattern']}</strong><br>
                    Frequency: {pattern['frequency']} | Impact: {pattern['impact']}
                </div>
            """
        
        # Add predictions
        html_content += "<h2>Predictive Insights</h2>"
        for pred in analysis["proactive_predictions"][:5]:
            html_content += f"""
                <div class="prediction">
                    <strong>{pred['prediction']}</strong><br>
                    <span class="confidence">Confidence: {pred['confidence']*100:.0f}%</span><br>
                    Recommendation: {pred['recommendation']}
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
    
    def add_subscriber(self, email, subscription_type="weekly", preferences=None):
        """Add a new subscriber"""
        subscriber = {
            "email": email,
            "subscription_type": subscription_type,
            "preferences": preferences or {},
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        
        if subscription_type not in self.subscribers:
            self.subscribers[subscription_type] = []
        
        self.subscribers[subscription_type].append(subscriber)
        self._save_json(self.subscribers, self.subscribers_file)
        
        logger.info(f"Added subscriber: {email} for {subscription_type} reports")
        return True
    
    def send_report(self, filepath, subscriber_email):
        """Send report via email"""
        try:
            # Email configuration (use environment variables in production)
            smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.environ.get("SMTP_PORT", "587"))
            smtp_user = os.environ.get("SMTP_USER")
            smtp_pass = os.environ.get("SMTP_PASS")
            
            if not smtp_user or not smtp_pass:
                logger.error("SMTP credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = subscriber_email
            msg['Subject'] = f"Claude Memory Insights Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Body
            body = """
            Hello,
            
            Your Claude Memory Insights Report is attached.
            
            This report includes:
            - Memory activity analysis
            - Quality assurance scores
            - Pattern recognition insights
            - Predictive recommendations
            - Knowledge gap analysis
            
            Best regards,
            Claude Memory System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach report
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(filepath)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Report sent to {subscriber_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send report: {e}")
            return False
    
    def run_scheduled_reports(self):
        """Run scheduled report generation and delivery"""
        logger.info("Running scheduled reports...")
        
        # Weekly reports (run on Mondays)
        if datetime.now().weekday() == 0:  # Monday
            analysis = self.analyze_memory_patterns("week")
            report_path = self.generate_report(analysis, "pdf")
            
            for subscriber in self.subscribers.get("weekly", []):
                if subscriber["active"]:
                    self.send_report(report_path, subscriber["email"])
        
        # Monthly reports (run on 1st of month)
        if datetime.now().day == 1:
            analysis = self.analyze_memory_patterns("month")
            report_path = self.generate_report(analysis, "pdf")
            
            for subscriber in self.subscribers.get("monthly", []):
                if subscriber["active"]:
                    self.send_report(report_path, subscriber["email"])
    
    def generate_compliance_audit_trail(self, start_date, end_date):
        """Generate compliance audit trail for memory access"""
        audit_trail = {
            "period": f"{start_date} to {end_date}",
            "generated_at": datetime.now().isoformat(),
            "access_logs": [],
            "modifications": [],
            "privacy_compliance": {
                "private_memories_protected": True,
                "mom_memories_isolated": True,
                "financial_access_logged": True,
                "legal_access_logged": True
            },
            "data_integrity": {
                "no_modifications_allowed": True,
                "all_memories_tagged": True,
                "source_attribution_complete": True
            }
        }
        
        # This would connect to actual access logs in production
        # For now, return template
        return audit_trail


# API Service for subscription management
class MemoryInsightsAPI:
    def __init__(self, generator):
        self.generator = generator
        self.stripe_key = os.environ.get("STRIPE_API_KEY")
        if self.stripe_key:
            stripe.api_key = self.stripe_key
    
    def create_subscription(self, email, plan="weekly", payment_method=None):
        """Create a paid subscription"""
        plans = {
            "weekly": {"price": 49, "interval": "week"},
            "monthly": {"price": 149, "interval": "month"},
            "enterprise": {"price": 999, "interval": "month"}
        }
        
        if plan not in plans:
            return {"error": "Invalid plan"}
        
        # In production, create Stripe subscription
        # For now, just add to subscribers
        self.generator.add_subscriber(email, plan)
        
        return {
            "status": "active",
            "plan": plan,
            "price": plans[plan]["price"],
            "next_report": self._next_report_date(plan)
        }
    
    def _next_report_date(self, plan):
        """Calculate next report date"""
        if plan == "weekly":
            days_until_monday = (7 - datetime.now().weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7
            return (datetime.now() + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")
        elif plan == "monthly":
            next_month = datetime.now().replace(day=1) + timedelta(days=32)
            return next_month.replace(day=1).strftime("%Y-%m-%d")
        return None


def main():
    """Main execution"""
    generator = MemoryInsightsGenerator()
    api = MemoryInsightsAPI(generator)
    
    # Schedule regular reports
    schedule.every().monday.at("08:00").do(generator.run_scheduled_reports)
    schedule.every().day.at("08:00").do(lambda: generator.run_scheduled_reports() if datetime.now().day == 1 else None)
    
    print("🎯 Claude Memory Automated Insights Generator")
    print("=" * 50)
    print("Available commands:")
    print("1. Generate test report")
    print("2. Add subscriber")
    print("3. Run analysis")
    print("4. Start scheduler")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nShutting down...")
            break


if __name__ == "__main__":
    # Example usage
    generator = MemoryInsightsGenerator()
    
    # Generate a test report
    print("Generating test report...")
    analysis = generator.analyze_memory_patterns("week")
    report_path = generator.generate_report(analysis, "pdf")
    print(f"Report generated: {report_path}")
    
    # Add a test subscriber
    # generator.add_subscriber("test@example.com", "weekly")
    
    # Generate compliance audit
    audit = generator.generate_compliance_audit_trail(
        datetime.now() - timedelta(days=30),
        datetime.now()
    )
    print(f"\nCompliance audit generated with {len(audit)} entries")