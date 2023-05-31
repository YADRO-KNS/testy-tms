export interface project {
    id: number;
    name: string;
    description: string;
}

export interface attachment {
    project: number;
    comment: string;
    name: string;
    filename: string;
    file_extension: string;
    size: number;
    content_type: number;
    object_id: number;
    user: number;
    file: string;
    link: string;
    url: string;
}

export interface testResult {
    id: number;
    project: number,
    status: number;
    status_color: { id: number, name: string, color: string };
    attachments: attachment[];
    test: number;
    user: number;
    user_full_name: string;
    comment?: string;
    is_archive: boolean;
    test_case_version: number;
    created_at: string,
    updated_at: string;
    execution_time?: number;
}

export interface myCase {
    id: number;
    name: string;
    suite: number;
    scenario: string;
    project: number;
    estimate: number | null;
    description: string;
    teardown: string;
    setup: string;
    url?: string;
    attachments: attachment[];
}

export interface test {
    id: number;
    case: number;
    name: string;
    plan: number;
    project: number;
    test_results: testResult[];
    current_result: string;
    last_status: string;
    last_status_color: { id: number, name: string, color: string };
    user?: number;
    username?: string;
    is_archive: boolean;
    updated_at?: string;
    created_at: string
}

export interface param {
    id: number,
    data: string,
    group_name: string,
    url?: string;
}

export interface testPlan {
    id: number,
    name: string,
    project: number,
    parent?: number,
    description: string,
    parameters?: number[],
    tests: test[],
    started_at: string,
    due_date: string,
    url: string,
    is_archive: boolean,
    child_test_plans: number[],
    title: string
}

export interface user {
    id: number;
    first_name?: string;
    last_name?: string;
    email: string;
    username: string;
    password: string;
}

export interface planStatistic {
    label: string,
    value: number
}