workflow Dragon {

    File input_matrix_a
    File input_matrix_b
    String sample_arrangement

    call runDragon {
        input:
            input_matrix_a = input_matrix_a,
            input_matrix_b = input_matrix_b,
            sample_arrangement = sample_arrangement
    }

    output {
        File fdr_values = runDragon.fdr_values
        File edge_weights = runDragon.edge_weights
    }
}

task runDragon {
        
    File input_matrix_a
    File input_matrix_b
    String sample_arrangement

    Int disk_size = 50

    command <<<
        python3 /opt/software/dragon.py -a ${input_matrix_a} \
            -b ${input_matrix_b} \
            -s "${sample_arrangement}"
    >>>

    output {
        File fdr_values = "dragon_adj_pvals.tsv"
        File edge_weights = "dragon_partial_correlations.tsv"
    }

    runtime {
        docker: "ghcr.io/web-mev/mev-dragon"
        cpu: 32
        memory: "96 G"
        disks: "local-disk " + disk_size + " HDD"
    }
}



