workflow Dragon {

    File input_matrix_a
    File input_matrix_b

    call runDragon {
        input:
            input_matrix_a = input_matrix_a,
            input_matrix_b = input_matrix_b
    }

    output {
        File fdr_values = runDragon.fdr_values
        File edge_weights = runDragon.edge_weights
    }
}

task runDragon {
        
    File input_matrix_a
    File input_matrix_b

    Int disk_size = 50

    command <<<
        python3 /opt/software/dragon.py -a ${input_matrix_a} \
            -b ${input_matrix_b}
    >>>

    output {
        File fdr_values = "adj_pvals.tsv"
        File edge_weights = "partial_corr.tsv"
    }

    runtime {
        docker: "blawney/dragon"
        cpu: 4
        memory: "30 G"
        disks: "local-disk " + disk_size + " HDD"
    }
}



