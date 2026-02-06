-- Initial Schema for Project Chimera - Autonomous AI Influencers
-- Based on Hierarchical Swarm Pattern defined in agent_patterns.md

-- 1. Influencer Orchestrator Entities
-- Stores the identity and long-term goals managed by the Orchestrator Agent
CREATE TABLE influencers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    persona_description TEXT NOT NULL,
    long_term_goals TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Represents the workflow units dispatched by the Orchestrator
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER REFERENCES influencers(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    -- Status flow: pending -> researching -> drafting -> safety_check -> approved/rejected
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Research Agent Entities
-- Stores trend discovery and audience analysis outputs
CREATE TABLE research_findings (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    trends_data JSONB, -- Structured trend analysis
    topic_ideation TEXT,
    audience_signals TEXT,
    source_urls TEXT[], -- Array of sources analyzed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Generation Agent Entities
-- Stores content drafts and reasoning metadata
CREATE TABLE content_drafts (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    research_finding_id INTEGER REFERENCES research_findings(id),
    content_body TEXT NOT NULL,
    media_prompts TEXT, -- For image/video generation
    style_reasoning TEXT, -- "Must attach reasoning metadata" constraint
    platform VARCHAR(50), -- e.g., 'twitter', 'instagram'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Safety Agent Entities
-- Implements the "Gatekeeper" and "Human-in-the-Loop" patterns
CREATE TABLE safety_reviews (
    id SERIAL PRIMARY KEY,
    draft_id INTEGER REFERENCES content_drafts(id) ON DELETE CASCADE,
    verdict VARCHAR(50) NOT NULL, -- 'approved', 'rejected', 'escalated_to_human'
    confidence_score DECIMAL(5, 4), -- 0.0000 to 1.0000
    policy_violations JSONB, -- List of detected risks/violations
    human_reviewer_notes TEXT, -- For HITL scenarios
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);